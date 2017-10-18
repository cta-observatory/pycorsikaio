from .subblocks import (
    parse_run_header,
    parse_event_header
)

from .constants import BLOCK_SIZE_BYTES


def read_block(f, fortran_raw=False):
    if fortran_raw is True:
        pos = f.tell() - 4

        if pos % 22932 == 0:
            f.read(8)

    return f.read(BLOCK_SIZE_BYTES)


def is_fortran_raw(f):
    pos = f.tell()
    f.seek(0)
    fortran_raw = f.read(4) != b'RUNH'
    f.seek(pos)
    return fortran_raw


def read_corsika_headers(inputfile):
    inputfile.seek(0)

    fortran_raw = is_fortran_raw(inputfile)

    if fortran_raw:
        inputfile.seek(4)

    byte_data = read_block(BLOCK_SIZE_BYTES)
    run_header = parse_run_header(byte_data)

    # Read Eventheader
    event_header_data = b''
    while True:
        byte_data = read_block(inputfile, fortran_raw)

        # No more Shower in file
        if byte_data[0:4] == b'RUNE':
            break

        if byte_data[0:4] != b'EVTH':
            continue

        event_header_data += byte_data

    event_headers = parse_event_header(event_header_data)

    return run_header, event_headers
