import numpy as np
import struct

from .run_header import (
    run_header_dtype_65,
    run_header_dtype_74,
    run_header_dtype_75,
)
from .event_header import (
    event_header_dtype_65,
    event_header_dtype_74,
    event_header_dtype_75,
)

from .cherenkov_photons import cherenkov_photons_dtype

from ..constants import RUNH_VERSION_POSITION, EVTH_VERSION_POSITION

__all__ = [
    'parse_event_header',
    'parse_run_header'
]

run_header_types = {
    6.5: run_header_dtype_65,
    7.4: run_header_dtype_74,
    7.5: run_header_dtype_75,
}

event_header_types = {
    6.5: event_header_dtype_65,
    7.4: event_header_dtype_74,
    7.5: event_header_dtype_75,
}


def parse_run_header(run_header_bytes):
    version = get_version(run_header_bytes, RUNH_VERSION_POSITION)
    version = round(version, 1)
    return np.frombuffer(run_header_bytes, dtype=run_header_types[version])[0]


def parse_event_header(event_header_bytes):
    version = get_version(event_header_bytes, EVTH_VERSION_POSITION)
    version = round(version, 1)
    return np.frombuffer(event_header_bytes, dtype=event_header_types[version])[0]


def get_version(header_bytes, version_pos):
    sl = slice(4 * (version_pos - 1), 4 * version_pos)
    return round(struct.unpack('f', header_bytes[sl])[0], 2)


def parse_cherenkov_photons(data_block_bytes):
    photons = np.frombuffer(data_block_bytes, dtype=cherenkov_photons_dtype)

    empty = photons == np.zeros(1, dtype=cherenkov_photons_dtype)
    return photons[~empty]
