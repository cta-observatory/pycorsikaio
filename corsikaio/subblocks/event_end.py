import warnings

from functools import lru_cache

from .dtypes import build_dtype, Field

event_end_fields = [
    Field(1, "event_end", dtype="S4", min_version=6.5000),
    Field(2, "event_number", min_version=6.5000),
    Field(3, "n_photons_weighted", min_version=6.5000),
    Field(4, "n_electrons_weighted", min_version=6.5000),
    Field(5, "n_hadrons_weighted", min_version=6.5000),
    Field(6, "n_muons_weighted", min_version=6.5000),
    Field(7, "n_particles_written", min_version=6.5000),
    Field(256, "longitudinal_fit_parameters", shape=6, min_version=7.3000),
    Field(262, "chi_square_longitudinal", min_version=6.5000),
    Field(263, "n_photons_written", min_version=6.5000),
    Field(264, "n_electrons_written", min_version=6.5000),
    Field(265, "n_hadrons_written", min_version=6.5000),
    Field(266, "n_muons_written", min_version=6.5000),
    Field(267, "n_em_particles_preshower", min_version=6.5000),
]


_min_supported_version = min(field.min_version for field in event_end_fields)


def _normalize_version(version):
    if version is None:
        warnings.warn("Version unknown, using earliest event end definition")
        return _min_supported_version
    if version < _min_supported_version:
        warnings.warn(
            f"Version {version} older than supported {_min_supported_version}; "
            "using earliest definition"
        )
        return _min_supported_version
    return version


def get_event_end_fields(version):
    version = _normalize_version(version)
    return [field for field in event_end_fields if field.min_version <= version]


@lru_cache(maxsize=None)
def get_event_end_types(version):
    version = _normalize_version(version)
    return build_dtype(get_event_end_fields(version))


@lru_cache(maxsize=None)
def get_event_end_thin_types(version):
    version = _normalize_version(version)
    return build_dtype(get_event_end_fields(version), itemsize=4 * 312)