import gzip
import numpy as np
from collections import namedtuple

from .subblocks import (
    parse_run_header,
    parse_event_header,
    parse_event_end,
    parse_cherenkov_photons,
    parse_longitudinal,
    parse_run_end,
    get_version,
)
from .subblocks.longitudinal import longitudinal_header_dtype
from .subblocks.data import mmcs_cherenkov_photons_dtype
from .io import read_block, read_buffer_size

from .constants import BLOCK_SIZE_BYTES, EVTH_VERSION_POSITION

Event = namedtuple('Event', ['header', 'data', 'longitudinal', 'end'])
PhotonEvent = namedtuple('PhotonEvent', ['header', 'photons', 'longitudinal', 'end'])


def is_gzip(f):
    pos = f.tell()
    f.seek(0)
    b1, b2 = f.read(2)
    f.seek(pos)

    return (b1 == 0x1f) and (b2 == 0x8b)


class CorsikaFile:

    def __init__(self, path):
        self.EventClass = Event

        self._f = open(path, 'rb')
        if is_gzip(self._f):
            self._f = gzip.open(path)

        self._buffer_size = read_buffer_size(self._f)

        runh_bytes = self.read_block()
        if not runh_bytes[:4] == b'RUNH':
            raise ValueError('File does not start with b"RUNH"')

        self.run_header = parse_run_header(runh_bytes)[0]
        self.version = round(float(self.run_header['version']), 4)

    def __next__(self):
        block = self.read_block()

        if block[:4] == b'RUNE' or len(block) < BLOCK_SIZE_BYTES:
            self._finished = True
            raise StopIteration()

        if block[:4] != b'EVTH':
            raise IOError('EVTH block expected but found {}'.format(block[:4]))

        event_header = parse_event_header(block)[0]

        block = self.read_block()
        data_bytes = bytearray()
        long_bytes = bytearray()

        while block[:4] != b'EVTE':

            if block[:4] == b'LONG':
                long_bytes.extend(block[longitudinal_header_dtype.itemsize // 4 + 1:])
            else:
                data_bytes.extend(block)

            block = self.read_block()

        event_end = parse_event_end(block)[0]
        data = self.parse_data_blocks(data_bytes)
        longitudinal = parse_longitudinal(long_bytes)

        return self.EventClass(event_header, data, longitudinal, event_end)

    @classmethod
    def parse_data_blocks(cls, data_bytes):
        array = np.frombuffer(data_bytes, dtype='float32').reshape(-1, 7)
        return array[np.any(array != 0, axis=1)]

    def __iter__(self):
        return self

    def read_headers(self):
        pos = self._f.tell()
        self._f.seek(0)

        block = self.read_block()
        event_header_data = bytearray()
        end_found = True

        while block:
            if block[:4] == b'RUNE':
                run_end = parse_run_end(block)
                break

            if block[:4] == b'EVTH' and get_version(block, EVTH_VERSION_POSITION) == self.version:
                if not end_found:
                    raise IOError('Expected EVTE block before next EVTH')

                event_header_data.extend(block)

                end_found = False
            elif block[:4] == b'EVTE':
                end_found = True

            block = self.read_block()

        self._f.seek(pos)

        event_headers = parse_event_header(event_header_data)

        return self.run_header, event_headers, run_end

    def read_block(self):
        return read_block(self._f, self._buffer_size)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self._f.close()


class CorsikaCherenkovFile(CorsikaFile):

    def __init__(self, path, mmcs=False):
        super().__init__(path)

        self.EventClass = PhotonEvent
        self.mmcs = mmcs

    def parse_data_blocks(self, data_bytes):
        photons = parse_cherenkov_photons(data_bytes)
        if not self.mmcs:
            return photons

        mmcs = np.empty(len(photons), dtype=mmcs_cherenkov_photons_dtype)

        for col in ('x', 'y', 'u', 'v', 't', 'production_height'):
            mmcs[col] = photons[col]

        mmcs['n_photons'] = 1.0
        mmcs['wavelength'] = photons['n_photons'] % 1000
        mmcs['mother_particle'] = photons['n_photons'] // 100000

        return mmcs
