import numpy as np
import struct

from .run_header import run_header_types
from .run_end import run_end_dtype

from .event_header import event_header_types
from .event_end import event_end_types

from .data import cherenkov_photons_dtype, particle_data_dtype
from .longitudinal import longitudinal_data_dtype

from ..constants import RUNH_VERSION_POSITION, EVTH_VERSION_POSITION

__all__ = [
    "parse_event_header",
    "parse_run_header",
    "parse_cherenkov_photons",
    "parse_particle_data",
    "parse_longitudinal",
]


def parse_run_header(run_header_bytes):
    version = get_version(run_header_bytes, RUNH_VERSION_POSITION)
    # get corsika minor version (Truncate the float after first digit)
    version = float(str(version)[:3])
    return np.frombuffer(run_header_bytes, dtype=run_header_types[version])


def parse_run_end(run_end_bytes):
    return np.frombuffer(run_end_bytes, dtype=run_end_dtype)


def parse_event_header(event_header_bytes):
    version = get_version(event_header_bytes, EVTH_VERSION_POSITION)
    version = float(str(version)[:3])
    return np.frombuffer(event_header_bytes, dtype=event_header_types[version])


def parse_event_end(event_end_bytes,version):
    return np.frombuffer(event_end_bytes, dtype=event_end_types[float(str(version)[:3])])


def get_version(header_bytes, version_pos):
    sl = slice(4 * (version_pos - 1), 4 * version_pos)
    return round(struct.unpack("f", header_bytes[sl])[0], 4)


def parse_data_block(data_block_bytes, dtype):
    data = np.frombuffer(data_block_bytes, dtype=dtype)
    empty = data == np.zeros(1, dtype=dtype)
    return data[~empty]


def parse_cherenkov_photons(data_block_bytes):
    return parse_data_block(data_block_bytes, dtype=cherenkov_photons_dtype)


def parse_particle_data(data_block_bytes):
    return parse_data_block(data_block_bytes, dtype=particle_data_dtype)


def parse_longitudinal(longitudinal_data_bytes):
    return parse_data_block(longitudinal_data_bytes, longitudinal_data_dtype)


def get_units_from_fields(subblock_fields):
    """Retrieve units as a dictionary from the fields of a file subblock.

    Dimensionless fields are not selected.

    Parameters
    ----------
    subblock_fields: list(Field)
        One of the defined lists of fields.

    Return
    ------
    units: dict
        Dictionary with field names as keys and
        string representations of units as values.
    """
    units = {field.name: field.unit for field in subblock_fields if field.unit is not None}
    return units
