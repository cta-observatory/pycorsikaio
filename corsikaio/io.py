import gzip
import struct

from .constants import BLOCK_SIZE_BYTES, BLOCK_SIZE_BYTES_THIN


#: buffersize for files not written as fortran sequential file
DEFAULT_BUFFER_SIZE = BLOCK_SIZE_BYTES * 100
DEFAULT_BUFFER_SIZE_THIN = BLOCK_SIZE_BYTES_THIN * 100
#: struct definition of the fortran record marker
RECORD_MARKER = struct.Struct('i')


def is_gzip(path):
    '''Test if a file is gzipped by reading its first two bytes and compare
    to the gzip marker bytes.
    '''
    with open(path, 'rb') as f:
        marker_bytes = f.read(2)

    return marker_bytes[0] == 0x1f and marker_bytes[1] == 0x8b


def is_zstd(path):
    '''Test if a file is compressed using zstd using its magic marker bytes
    '''
    with open(path, 'rb') as f:
        marker_bytes = f.read(4)

    return marker_bytes == b'\x28\xb5\x2f\xfd'


def open_compressed(path):
    if is_gzip(path):
        return gzip.open(path)

    if is_zstd(path):
        from zstandard import ZstdDecompressor
        return ZstdDecompressor().stream_reader(open(path, 'rb'))

    return open(path, 'rb')


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
    if thinning == False:
        block_size = BLOCK_SIZE_BYTES
        buffer_size = DEFAULT_BUFFER_SIZE
    else:
        block_size = BLOCK_SIZE_BYTES_THIN
        buffer_size = DEFAULT_BUFFER_SIZE_THIN


    data = f.read(4)
    f.seek(0)
    if data == b'RUNH':
        is_fortran_file = False

    while True:
        # for the fortran-chunked output, we need to read the record size
        if is_fortran_file:
            data = f.read(RECORD_MARKER.size)
            if len(data) == 0:
                return

            if len(data) < RECORD_MARKER.size:
                raise IOError("Read less bytes than expected, file seems to be truncated")

            buffer_size, = RECORD_MARKER.unpack(data)

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
