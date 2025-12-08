from functools import cache
import numpy as np

from .dtypes import build_dtype, Field, filter_fields_by_version

event_end_fields = [
    Field(1, "event_end", dtype="S4", min_version=np.float32(6.5)),
    Field(2, "event_number", min_version=np.float32(6.5)),
    Field(3, "n_photons_weighted", min_version=np.float32(6.5)),
    Field(4, "n_electrons_weighted", min_version=np.float32(6.5)),
    Field(5, "n_hadrons_weighted", min_version=np.float32(6.5)),
    Field(6, "n_muons_weighted", min_version=np.float32(6.5)),
    Field(7, "n_particles_written", min_version=np.float32(6.5)),
    Field(256, "longitudinal_fit_parameters", shape=6, min_version=np.float32(7.3)),
    Field(262, "chi_square_longitudinal", min_version=np.float32(6.5)),
    Field(263, "n_photons_written", min_version=np.float32(6.5)),
    Field(264, "n_electrons_written", min_version=np.float32(6.5)),
    Field(265, "n_hadrons_written", min_version=np.float32(6.5)),
    Field(266, "n_muons_written", min_version=np.float32(6.5)),
    Field(267, "n_em_particles_preshower", min_version=np.float32(6.5)),
]


def get_event_end_fields(version):
    return filter_fields_by_version(event_end_fields, version)


@cache
def get_event_end_dtype(version):
    return build_dtype(get_event_end_fields(version))


@cache
def get_event_end_thin_dtype(version):
    return build_dtype(get_event_end_fields(version), itemsize=4 * 312)
