from functools import cache
import numpy as np

from .dtypes import Field, build_dtype, filter_fields_by_version


run_header_fields = [
    Field(1, "run_header", dtype="S4", min_version=np.float32(6.5)),
    Field(2, "run_number", min_version=np.float32(6.5)),
    Field(3, "date", min_version=np.float32(6.5)),
    Field(4, "version", min_version=np.float32(6.5)),
    Field(5, "n_observation_levels", min_version=np.float32(6.5)),
    Field(5 + 1, "observation_height", unit="cm", shape=10, min_version=np.float32(6.5)),
    Field(16, "energy_spectrum_slope", min_version=np.float32(6.5)),
    Field(17, "energy_min", unit="GeV", min_version=np.float32(6.5)),
    Field(18, "energy_max", unit="GeV", min_version=np.float32(6.5)),
    Field(19, "egs4_flag", min_version=np.float32(6.5)),
    Field(20, "nkg_flag", min_version=np.float32(6.5)),
    Field(21, "energy_cutoff_hadrons", unit="GeV", min_version=np.float32(6.5)),
    Field(22, "energy_cutoff_muons", unit="GeV", min_version=np.float32(6.5)),
    Field(23, "energy_cutoff_electrons", unit="GeV", min_version=np.float32(6.5)),
    Field(24, "energy_cutoff_photons", unit="GeV", min_version=np.float32(6.5)),
    Field(25, "physical_constants_and_interaction_flags", shape=50, min_version=np.float32(6.5)),
    Field(75, "inclined_observation_plane_x", unit="cm", min_version=np.float32(7.3)),
    Field(76, "inclined_observation_plane_y", unit="cm", min_version=np.float32(7.3)),
    Field(77, "inclined_observation_plane_z", unit="cm", min_version=np.float32(7.3)),
    Field(78, "inclined_observation_plane_theta", unit="deg", min_version=np.float32(7.3)),
    Field(79, "inclined_observation_plane_phi", unit="deg", min_version=np.float32(7.3)),
    Field(92, "rotation_angle_to_true_north", unit="deg", min_version=np.float32(7.75)),
    Field(93, "n_showers", min_version=np.float32(7.4)),  # typo in the 7.400 manual
    Field(94 + 1, "cka", shape=40, min_version=np.float32(6.5)),
    Field(134 + 1, "ceta", shape=5, min_version=np.float32(6.5)),
    Field(139 + 1, "cstrba", shape=11, min_version=np.float32(6.5)),
    Field(248, "x_scatter", unit="cm", min_version=np.float32(7.3)),
    Field(249, "y_scatter", unit="cm", min_version=np.float32(7.3)),
    Field(254 + 1, "aatm", shape=5, min_version=np.float32(6.5)),
    Field(259 + 1, "batm", shape=5, min_version=np.float32(6.5)),
    Field(264 + 1, "catm", shape=5, min_version=np.float32(6.5)),
    Field(270, "nflain", min_version=np.float32(6.5)),
    Field(271, "nfdif", min_version=np.float32(6.5)),
    Field(272, "nflpi0_100nflpif", min_version=np.float32(6.5)),
    Field(273, "nflche_100nfragm", min_version=np.float32(6.5)),
]


def get_run_header_fields(version):
    return filter_fields_by_version(run_header_fields, version)


@cache
def get_run_header_dtype(version):
    return build_dtype(get_run_header_fields(version))


@cache
def get_run_header_thin_dtype(version):
    return build_dtype(get_run_header_fields(version), itemsize=4 * 312)
