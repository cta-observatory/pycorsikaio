import numpy as np

from .run_header import get_run_header_dtype, get_run_header_thin_dtype
from .run_end import run_end_dtype, run_end_thin_dtype

from .event_header import get_event_header_dtype, get_event_header_thin_dtype
from .event_end import get_event_end_dtype, get_event_end_thin_dtype

from .data import cherenkov_photons_dtype, cherenkov_photons_thin_dtype, particle_data_dtype, particle_data_thin_dtype
from .longitudinal import longitudinal_data_dtype

from ..constants import RUNH_VERSION_POSITION, EVTH_VERSION_POSITION

__all__ = [
    "parse_event_header",
    "parse_event_header_thin",
    "parse_run_header",
    "parse_run_header_thin",
    "parse_cherenkov_photons",
    "parse_cherenkov_photons_thin",
    "parse_particle_data",
    "parse_particle_data_thin",
    "parse_longitudinal",
]


def parse_run_header(run_header_bytes):
    version = get_version(run_header_bytes, RUNH_VERSION_POSITION)
    return np.frombuffer(run_header_bytes, dtype=get_run_header_dtype(version))


def parse_run_header_thin(run_header_bytes):
    version = get_version(run_header_bytes, RUNH_VERSION_POSITION)
    return np.frombuffer(run_header_bytes, dtype=get_run_header_thin_dtype(version))


def parse_run_end(run_end_bytes):
    return np.frombuffer(run_end_bytes, dtype=run_end_dtype)


def parse_run_end_thin(run_end_bytes):
    return np.frombuffer(run_end_bytes, dtype=run_end_thin_dtype)


def parse_event_header(event_header_bytes):
    version = get_version(event_header_bytes, EVTH_VERSION_POSITION)
    return np.frombuffer(event_header_bytes, dtype=get_event_header_dtype(version))


def parse_event_header_thin(event_header_bytes):
    version = get_version(event_header_bytes, EVTH_VERSION_POSITION)
    return np.frombuffer(event_header_bytes, dtype=get_event_header_thin_dtype(version))


def parse_event_end(event_end_bytes, version):
    return np.frombuffer(event_end_bytes, dtype=get_event_end_dtype(version))


def parse_event_end_thin(event_end_bytes, version):
    return np.frombuffer(event_end_bytes, dtype=get_event_end_thin_dtype(version))


def get_version(header_bytes, version_pos):
    sl = slice(4 * (version_pos - 1), 4 * version_pos)
    return np.frombuffer(header_bytes[sl], dtype=np.float32)[0]


def parse_data_block(data_block_bytes, dtype):
    data = np.frombuffer(data_block_bytes, dtype=dtype)
    empty = data == np.zeros(1, dtype=dtype)
    return data[~empty]


def parse_cherenkov_photons(data_block_bytes):
    return parse_data_block(data_block_bytes, dtype=cherenkov_photons_dtype)


def parse_cherenkov_photons_thin(data_block_bytes):
    return parse_data_block(data_block_bytes, dtype=cherenkov_photons_thin_dtype)


def parse_particle_data(data_block_bytes):
    return parse_data_block(data_block_bytes, dtype=particle_data_dtype)


def parse_particle_data_thin(data_block_bytes):
    return parse_data_block(data_block_bytes, dtype=particle_data_thin_dtype)


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
