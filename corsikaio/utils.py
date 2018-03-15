from .file import CorsikaFile


def read_corsika_headers(path):


    buffer_size = read_buffer_size(inputfile)
    byte_data = read_block(inputfile, buffer_size)
    run_header = parse_run_header(byte_data)

    # Read Eventheader
    event_header_data = bytearray()
    while True:
        byte_data = read_block(inputfile, buffer_size)

        # No more Shower in file
        if byte_data[0:4] == b'RUNE':
            break

        if byte_data[0:4] != b'EVTH':
            continue

        event_header_data.extend(byte_data)

    event_headers = parse_event_header(event_header_data)

    return run_header, event_headers
