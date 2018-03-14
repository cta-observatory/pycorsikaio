import gzip
import numpy as np
from numpy.lib.recfunctions import append_fields
from collections import namedtuple

from .subblocks import parse_run_header, parse_event_header, parse_cherenkov_photons
from .io import read_block, read_buffer_size

from .constants import BLOCK_SIZE_BYTES

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

        self.run_header = parse_run_header(runh_bytes)
        self.version = round(float(self.run_header['version']), 4)

    def __next__(self):
        block = self.read_block()

        if block[:4] == b'RUNE' or len(block) < BLOCK_SIZE_BYTES:
            self._finished = True
            raise StopIteration()

        if block[:4] != b'EVTH':
            raise IOError('EVTH block expected but found {}'.format(block[:4]))

        event_header = parse_event_header(block)

        block = self.read_block()
        data_bytes = bytearray()
        long_blocks = []
        while block[:4] != b'EVTE':
            if block[:4] == b'LONG':
                long_blocks.append(block)
            else:
                data_bytes.extend(block)
            block = self.read_block()

        event_end = block

        data = self.parse_data_blocks(data_bytes)

        return self.EventClass(event_header, data, long_blocks, event_end)

    @classmethod
    def parse_data_blocks(cls, data_bytes):
        array = np.frombuffer(data_bytes, dtype='float32').reshape(-1, 7)
        return array[np.any(array != 0, axis=1)]

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


class CorsikaCherenkovFile(CorsikaFile):

    def __init__(self, path, mmcs=False):
        super().__init__(path)

        self.EventClass = PhotonEvent
        self.mmcs = mmcs

    def parse_data_blocks(self, data_bytes):
        photons = parse_cherenkov_photons(data_bytes)

        # mmcs encodes wavelength and mother particle in the n column
        if self.mmcs:
            photons = append_fields(
                photons,
                names=['wavelength', 'mother_particle'],
                data=[
                    photons['n_photons'] % 1000,
                    photons['n_photons'] // 100000
                ],
                usemask=False,
                asrecarray=False,
            )
            photons['n_photons'] = 1.0
        return photons
