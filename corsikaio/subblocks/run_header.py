import warnings
from .dtypes import Field, build_dtype

from functools import lru_cache


run_header_fields = [
    Field(1, "run_header", dtype="S4", min_version=6.5000),
    Field(2, "run_number", min_version=6.5000),
    Field(3, "date", min_version=6.5000),
    Field(4, "version", min_version=6.5000),
    Field(5, "n_observation_levels", min_version=6.5000),
    Field(5 + 1, "observation_height", unit="cm", shape=10, min_version=6.5000),
    Field(16, "energy_spectrum_slope", min_version=6.5000),
    Field(17, "energy_min", unit="GeV", min_version=6.5000),
    Field(18, "energy_max", unit="GeV", min_version=6.5000),
    Field(19, "egs4_flag", min_version=6.5000),
    Field(20, "nkg_flag", min_version=6.5000),
    Field(21, "energy_cutoff_hadrons", unit="GeV", min_version=6.5000),
    Field(22, "energy_cutoff_muons", unit="GeV", min_version=6.5000),
    Field(23, "energy_cutoff_electrons", unit="GeV", min_version=6.5000),
    Field(24, "energy_cutoff_photons", unit="GeV", min_version=6.5000),
    Field(25, "physical_constants_and_interaction_flags", shape=50, min_version=6.5000),
    Field(75, "inclined_observation_plane_x", unit="cm", min_version=7.3000),
    Field(76, "inclined_observation_plane_y", unit="cm", min_version=7.3000),
    Field(77, "inclined_observation_plane_z", unit="cm", min_version=7.3000),
    Field(78, "inclined_observation_plane_theta", unit="deg", min_version=7.3000),
    Field(79, "inclined_observation_plane_phi", unit="deg", min_version=7.3000),
    Field(93, "n_showers", min_version=7.4000),  # typo in the 7.400 manual
    Field(94 + 1, "cka", shape=40, min_version=6.5000),
    Field(134 + 1, "ceta", shape=5, min_version=6.5000),
    Field(139 + 1, "cstrba", shape=11, min_version=6.5000),
    Field(248, "x_scatter", unit="cm", min_version=7.3000),
    Field(249, "y_scatter", unit="cm", min_version=7.3000),
    Field(254 + 1, "aatm", shape=5, min_version=6.5000),
    Field(259 + 1, "batm", shape=5, min_version=6.5000),
    Field(264 + 1, "catm", shape=5, min_version=6.5000),
    Field(270, "nflain", min_version=6.5000),
    Field(271, "nfdif", min_version=6.5000),
    Field(272, "nflpi0_100nflpif", min_version=6.5000),
    Field(273, "nflche_100nfragm", min_version=6.5000),
]


_min_supported_version = min(field.min_version for field in run_header_fields)


def _normalize_version(version):
    if version is None:
        warnings.warn("Version unknown, using earliest run header definition")
        return _min_supported_version
    if version < _min_supported_version:
        warnings.warn(
            f"Version {version} older than supported {_min_supported_version}; "
            "using earliest definition"
        )
        return _min_supported_version
    return version


def get_run_header_fields(version):
    version = _normalize_version(version)
    return [field for field in run_header_fields if field.min_version <= version]


@lru_cache(maxsize=None)
def get_run_header_types(version):
    version = _normalize_version(version)
    return build_dtype(get_run_header_fields(version))


@lru_cache(maxsize=None)
def get_run_header_thin_types(version):
    version = _normalize_version(version)
    return build_dtype(get_run_header_fields(version), itemsize=4 * 312)