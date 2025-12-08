import gzip
import struct
from enum import Enum

from .constants import BLOCK_SIZE_BYTES, BLOCK_SIZE_BYTES_THIN


#: buffersize for files not written as fortran sequential file
DEFAULT_BUFFER_SIZE = BLOCK_SIZE_BYTES * 100
DEFAULT_BUFFER_SIZE_THIN = BLOCK_SIZE_BYTES_THIN * 100
#: struct definition of the fortran record marker
RECORD_MARKER = struct.Struct('i')


class MagicBytes(Enum):
    GZIP = b"\x1f\x8b"
    ZSTD = b"\x28\xb5\x2f\xfd"
    EVENTIO_LE = b"\x37\x8a\x1f\xd4"
    EVENTIO_BE = b"\xd4\x1f\x8a\x37"


MAX_MARKER_LENGTH = max(len(marker.value) for marker in MagicBytes)


def check_magic(magic, *, path=None, marker_bytes=None):
    if (path is None) == (marker_bytes is None):
        raise ValueError("Need to provide exactly one of path xor marker_bytes")

    if marker_bytes is None:
        with open(path, "rb") as f:
            marker_bytes = f.read(MAX_MARKER_LENGTH)

    expected = magic.value
    return marker_bytes[: len(expected)] == expected


def is_gzip(path):
    """Test if a file is gzip compressed."""
    return check_magic(MagicBytes.GZIP, path=path)


def is_zstd(path):
    """Test if a file is zstd compressed."""
    return check_magic(MagicBytes.ZSTD, path=path)


class ClosingGzipFile(gzip.GzipFile):
    """A wrapper around std lib GzipFile that auto-closes the underlying fobj."""

    def close(self):
        if self.fileobj is not None:
            self.fileobj.close()
        super().close()


def open_compressed(path):
    fobj = open(path, "rb")
    marker_bytes = fobj.read(MAX_MARKER_LENGTH)
    fobj.seek(0)

    if check_magic(MagicBytes.GZIP, marker_bytes=marker_bytes):
        return ClosingGzipFile(mode="rb", fileobj=fobj)

    if check_magic(MagicBytes.ZSTD, marker_bytes=marker_bytes):
        from zstandard import ZstdDecompressor

        return ZstdDecompressor().stream_reader(fobj, closefd=True)

    return fobj


def read_buffer_size(path):
    '''
    Reads the first 4 bytes of a file and checks if
    it is the 'RUNH' designation None is returned,
    if not interpret it as unsigned integer, the
    size of the CORSIKA buffer in bytes
    '''
    with open_compressed(path) as f:
        data = f.read(RECORD_MARKER.size)

        if data == b'RUNH':
            return None

        buffer_size, = RECORD_MARKER.unpack(data)

    return buffer_size


def iter_blocks(f, thinning=False):
    is_fortran_file = True
    if not thinning:
        block_size = BLOCK_SIZE_BYTES
        buffer_size = DEFAULT_BUFFER_SIZE
    else:
        block_size = BLOCK_SIZE_BYTES_THIN
        buffer_size = DEFAULT_BUFFER_SIZE_THIN

    data = f.read(4)
    first = True
    if data == b"RUNH":
        is_fortran_file = False
    elif data in (MagicBytes.EVENTIO_LE.value, MagicBytes.EVENTIO_BE.value):
        msg = "This file is in eventio format, try opening with eventio.IACTFile"
        raise ValueError(msg)

    while True:
        # for the fortran-chunked output, we need to read the record size
        if is_fortran_file:
            if first is True:
                data = data + f.read(RECORD_MARKER.size - len(data))
            else:
                data = f.read(RECORD_MARKER.size)

            if len(data) == 0:
                return

            if len(data) < RECORD_MARKER.size:
                raise IOError("Read less bytes than expected, file seems to be truncated")

            buffer_size, = RECORD_MARKER.unpack(data)
            data = b""

        if first is True:
            data = data + f.read(buffer_size - len(data))
            first = False
        else:
            data = f.read(buffer_size)

        if is_fortran_file:
            if len(data) < buffer_size:
                raise IOError("Read less bytes than expected, file seems to be truncated")

        else:
            if len(data) == 0:
                return

        n_blocks, rest = divmod(len(data), block_size)
        if rest != 0:
            raise IOError("Read less bytes than expected, file seems to be truncated")

        for block in range(n_blocks):
            start = block * block_size
            stop = start + block_size
            block = data[start:stop]
            yield block

        # read trailing record marker
        if is_fortran_file:
            f.read(RECORD_MARKER.size)


def read_block(f, thinning=False, buffer_size=None):
    '''
    Reads a block of CORSIKA output, e.g. 273 4-byte floats.

    Under some conditions, CORSIKA writes output as FORTRAN
    raw file format. This means, there is a 4-byte unsigned
    integer (the buffer size)
    before and after each block, which has to be skipped.
    '''
    if thinning == False:
        block_size = BLOCK_SIZE_BYTES
    else:
        block_size = BLOCK_SIZE_BYTES_THIN
    if buffer_size is not None:
        pos = f.tell()
        if pos == 0:
            f.seek(4)

        if (pos + 4) % (buffer_size + 8) == 0:
            f.read(8)

    block = f.read(block_size)
    if len(block) < block_size:
        raise IOError("Read less bytes than expected, file seems to be truncated")

    return block
