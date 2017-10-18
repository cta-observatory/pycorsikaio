import struct

from .subblocks import (
    parse_run_header,
    parse_event_header
)

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
    integer at each
    '''
    pos = f.tell()

    if buffer_size is not None:
        if pos == 0:
            f.seek(4)

        pos -= 4

        if pos % buffer_size == 0:
            f.read(8)

    return f.read(BLOCK_SIZE_BYTES)


def read_corsika_headers(inputfile):
    inputfile.seek(0)

    buffer_size = read_buffer_size(inputfile)
    byte_data = read_block(inputfile, buffer_size)
    run_header = parse_run_header(byte_data)

    # Read Eventheader
    event_header_data = b''
    while True:
        byte_data = read_block(inputfile, buffer_size)

        # No more Shower in file
        if byte_data[0:4] == b'RUNE':
            break

        if byte_data[0:4] != b'EVTH':
            continue

        event_header_data += byte_data

    event_headers = parse_event_header(event_header_data)

    return run_header, event_headers
