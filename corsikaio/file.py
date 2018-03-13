import gzip
from collections import defaultdict

from .subblocks import parse_run_header, parse_event_header
from .io import read_block, read_buffer_size


def is_gzip(f):
    pos = f.tell()
    f.seek(0)
    b1, b2 = f.read(2)
    f.seek(pos)

    return (b1 == 0x1f) and (b2 == 0x8b)


class CorsikaFile:
    def __init__(self, path):

        self._f = open(path, 'rb')
        if is_gzip(self._f):
            self._f = gzip.open(path)

        self._buffer_size = read_buffer_size(self._f)

        runh_bytes = self.read_block()
        if not runh_bytes[:4] == b'RUNH':
            raise ValueError('File does not start with b"RUNH"')

        self.run_header = parse_run_header(runh_bytes)
        self.version = round(float(self.run_header['version'][0]), 4)

    def __next__(self):
        block = self.read_block()

        if block[:4] == b'RUNE':
            raise StopIteration()

        if block[:4] != b'EVTH':
            raise IOError('EVTH block expected but found {}'.format(block[:4]))

        event_header = parse_event_header(block)

        block = self.read_block()
        data_blocks = defaultdict(list)
        while block[:4] != b'EVTE':
            data_blocks[block[:4]].append(block)
            block = self.read_block()

        event_end = block

        return event_header, data_blocks, event_end

    def __iter__(self):
        return self

    def iter_event_headers(self):
        pos = self._f.tell()
        self._f.seek(0)

        block = self.read_block()
        n_events = 0
        end_found = True
        while block:
            if block[:4] == b'EVTH':
                if not end_found:
                    raise IOError('Expected EVTE block before next EVTH')

                yield parse_event_header(block)
                n_events += 1

                end_found = False

            elif block[:4] == b'EVTE':
                end_found = True
            block = self.read_block()

        self._f.seek(pos)

    def read_block(self):
        return read_block(self._f, self._buffer_size)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self._f.close()
