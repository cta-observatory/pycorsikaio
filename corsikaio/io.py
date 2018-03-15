import struct

from .constants import BLOCK_SIZE_BYTES


def read_buffer_size(f):
    '''
    Reads the first 4 bytes of a file and checks if
    it is the 'RUNH' designation None is returned,
    if not interpret it as unsigned integer, the
    size of the CORSIKA buffer in bytes
    '''
    pos = f.tell()

    f.seek(0)
    data = f.read(4)
    f.seek(pos)

    if data == b'RUNH':
        return None

    buffer_size, = struct.unpack('I', data)

    return buffer_size


def read_block(f, buffer_size=None):
    '''
    Reads a block of CORSIKA output, e.g. 273 4-byte floats.

    Under some conditions, CORSIKA writes output as FORTRAN
    raw file format. This means, there is a 4-byte unsigned
    integer (the buffer size)
    before and after each block, which has to be skipped.
    '''
    pos = f.tell()

    if buffer_size is not None:
        if pos == 0:
            f.seek(4)

        if (pos + 4) % (buffer_size + 8) == 0:
            f.read(8)

    return f.read(BLOCK_SIZE_BYTES)
