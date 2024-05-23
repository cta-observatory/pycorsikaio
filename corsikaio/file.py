import numpy as np
from collections import namedtuple

from .subblocks import (
    parse_run_header,
    parse_run_header_thin,
    parse_event_header,
    parse_event_header_thin,
    parse_event_end,
    parse_event_end_thin,
    parse_cherenkov_photons,
    parse_cherenkov_photons_thin,
    parse_particle_data,
    parse_particle_data_thin,
    parse_longitudinal,
    parse_run_end,
    parse_run_end_thin,
    get_version,
)
from .subblocks.longitudinal import longitudinal_header_dtype
from .subblocks.data import mmcs_cherenkov_photons_dtype
from .io import iter_blocks, read_buffer_size, open_compressed

from .constants import BLOCK_SIZE_BYTES, BLOCK_SIZE_BYTES_THIN, EVTH_VERSION_POSITION

Event = namedtuple('Event', ['header', 'data', 'longitudinal', 'end'])
PhotonEvent = namedtuple('PhotonEvent', ['header', 'photons', 'longitudinal', 'end'])
ParticleEvent = namedtuple(
    'ParticleEvent',
    ['header', 'particles', 'longitudinal', 'end']
)

def _to_floatarray(block):
    return np.frombuffer(block, dtype=np.float32)


class CorsikaFile:
    """
    A file to iterate over events in a CORSIKA binary output file.
    """

    def __init__(self, path, parse_blocks=True, thinning=False):
        self.EventClass = Event

        self.parse_blocks = parse_blocks
        self.thinning = thinning
        self._buffer_size = read_buffer_size(path)
        self._f = open_compressed(path)
        self._block_iter = iter_blocks(self._f, thinning=self.thinning)

        runh_bytes = next(self._block_iter)
        if not runh_bytes[:4] == b'RUNH':
            raise ValueError('File does not start with b"RUNH"')

        if self.thinning == False:
            self.run_header = parse_run_header(runh_bytes)[0]
        else:
            self.run_header = parse_run_header_thin(runh_bytes)[0]
        self.version = round(float(self.run_header['version']), 4)
        self._run_end = None

    @property
    def run_end(self):
        if self.thinning == False:
            block_size = BLOCK_SIZE_BYTES
        else:
            block_size = BLOCK_SIZE_BYTES_THIN
        if self._run_end is None:
            pos = self._f.tell()

            if self._buffer_size is None:
                self._f.seek(0, 2)
            else:
                self._f.seek(-4, 2)

            self._f.seek(-block_size, 1)
            block = self._f.read(block_size)
            while block[:4] != b'RUNE':
                self._f.seek(-2 * block_size, 1)
                block = self._f.read(block_size)

            if self.thinning == False:
                self._run_end = parse_run_end(block)[0]
            else:
                self._run_end = parse_run_end_thin(block)[0]
            self._f.seek(pos)

        return self._run_end

    def __next__(self):
        try:
            block = next(self._block_iter)
        except StopIteration:
            raise IOError("File seems to be truncated")

        if block[:4] == b'RUNE':
            if self.thinning == False:
                self._run_end = parse_run_end(block)
            else:
                self._run_end = parse_run_end_thin(block)
            raise StopIteration()

        if block[:4] != b'EVTH':
            raise IOError('EVTH block expected but found {}'.format(block[:4]))

        if self.parse_blocks:
            if self.thinning == False:
                event_header = parse_event_header(block)[0]
            else:
                event_header = parse_event_header_thin(block)[0]
        else:
            event_header = _to_floatarray(block)

        data_bytes = bytearray()
        long_bytes = bytearray()

        try:
            block = next(self._block_iter)
        except StopIteration:
            raise IOError("File seems to be truncated")

        while block[:4] != b'EVTE':

            if block[:4] == b'LONG':
                long_bytes += block[longitudinal_header_dtype.itemsize:]
            else:
                data_bytes += block

            try:
                block = next(self._block_iter)
            except StopIteration:
                raise IOError("File seems to be truncated")

        if self.parse_blocks:
            if self.thinning == False:
                event_end = parse_event_end(block,self.version)[0]
            else:
                event_end = parse_event_end_thin(block,self.version)[0]
            data = self.parse_data_blocks(data_bytes)
            longitudinal = parse_longitudinal(long_bytes)
        else:
            event_end = _to_floatarray(block)
            if self.thinning == False:
                data = _to_floatarray(data_bytes).reshape(-1, 7)
            else:
                data = _to_floatarray(data_bytes).reshape(-1, 8)

            longitudinal = _to_floatarray(long_bytes)

        return self.EventClass(event_header, data, longitudinal, event_end)

    def parse_data_blocks(self, data_bytes):
        if self.thinning == False:
            array = np.frombuffer(data_bytes, dtype='float32').reshape(-1, 7)
        else:
            array = np.frombuffer(data_bytes, dtype='float32').reshape(-1, 8)
        return array[np.any(array != 0, axis=1)]

    def __iter__(self):
        return self

    def read_headers(self):
        pos = self._f.tell()
        self._f.seek(0)

        block_iter = iter_blocks(self._f, thinning=self.thinning)
        block = next(block_iter)
        event_header_data = bytearray()
        end_found = True

        while block:
            if block[:4] == b'RUNE':
                if self.thinning == False:
                    self._run_end = parse_run_end(block)[0]
                else:
                    self._run_end = parse_run_end_thin(block)[0]
                break

            if (
                block[:4] == b'EVTH'
                and get_version(block, EVTH_VERSION_POSITION) == self.version
            ):
                if not end_found:
                    raise IOError('Expected EVTE block before next EVTH')

                event_header_data += block

                end_found = False
            elif block[:4] == b'EVTE':
                end_found = True

            block = next(block_iter)

        self._f.seek(pos)

        if self.thinning == False:
            event_headers = parse_event_header(event_header_data)
        else:
            event_headers = parse_event_header_thin(event_header_data)

        return self.run_header, event_headers, self._run_end

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self._f.close()


class CorsikaCherenkovFile(CorsikaFile):

    def __init__(self, path, thinning=False, mmcs=False, **kwargs):
        super().__init__(path, thinning=thinning, **kwargs)

        self.EventClass = PhotonEvent
        self.mmcs = mmcs

    def parse_data_blocks(self, data_bytes):
        if self.thinning == False:
            photons = parse_cherenkov_photons(data_bytes)
        else:
            photons = parse_cherenkov_photons_thin(data_bytes)
        if not self.mmcs:
            return photons

        mmcs = np.empty(len(photons), dtype=mmcs_cherenkov_photons_dtype)

        for col in ('x', 'y', 'u', 'v', 't', 'production_height'):
            mmcs[col] = photons[col]

        mmcs['n_photons'] = 1.0
        mmcs['wavelength'] = photons['n_photons'] % 1000
        mmcs['mother_particle'] = photons['n_photons'] // 100000

        return mmcs


class CorsikaParticleFile(CorsikaFile):

    def __init__(self, path, thinning=False, **kwargs):
        super().__init__(path, thinning=thinning, **kwargs)
        self.EventClass = ParticleEvent

    def parse_data_blocks(self, data_bytes):
        if self.thinning == False:
            return parse_particle_data(data_bytes)
        else:
            return parse_particle_data_thin(data_bytes)
