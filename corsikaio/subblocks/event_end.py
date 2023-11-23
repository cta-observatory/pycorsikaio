import warnings
from collections import defaultdict

from .dtypes import build_dtype, Field

event_end_fields_65 = [
    Field(1, "event_end", dtype="S4"),
    Field(2, "event_number"),
    Field(3, "n_photons_weighted"),
    Field(4, "n_electrons_weighted"),
    Field(5, "n_hadrons_weighted"),
    Field(6, "n_muons_weighted"),
    Field(7, "n_particles_written"),
    Field(262, "chi_square_longitudinal"),
    Field(263, "n_photons_written"),
    Field(264, "n_electrons_written"),
    Field(265, "n_hadrons_written"),
    Field(266, "n_muons_written"),
    Field(267, "n_em_particles_preshower"),
]

event_end_fields_7x = [
    Field(1, "event_end", dtype="S4"),
    Field(2, "event_number"),
    Field(3, "n_photons_weighted"),
    Field(4, "n_electrons_weighted"),
    Field(5, "n_hadrons_weighted"),
    Field(6, "n_muons_weighted"),
    Field(7, "n_particles_written"),
    Field(256, "longitudinal_fit_parameters", shape=6),
    Field(262, "chi_square_longitudinal"),
    Field(263, "n_photons_written"),
    Field(264, "n_electrons_written"),
    Field(265, "n_hadrons_written"),
    Field(266, "n_muons_written"),
    Field(267, "n_em_particles_preshower"),
 ]

event_end_dtype_65 = build_dtype(event_end_fields_65)
event_end_dtype_7x = build_dtype(event_end_fields_7x)

def warn_dtype():
    warnings.warn("Version unknown, using default event end definition dtype of version 7.x")
    return event_end_dtype_7x

def warn_fields():
    warnings.warn("Version unknown, using default event end fields definition of version 7.x")
    return event_end_fields_7x

event_end_fields = defaultdict(warn_fields)
event_end_fields[6.5] = event_end_fields_65
event_end_fields[7.4] = event_end_fields_7x
event_end_fields[7.5] = event_end_fields_7x
event_end_fields[7.6] = event_end_fields_7x
event_end_fields[7.7] = event_end_fields_7x

event_end_types = defaultdict(warn_dtype)
event_end_types[6.5] = event_end_dtype_65
event_end_types[7.4] = event_end_dtype_7x
event_end_types[7.5] = event_end_dtype_7x
event_end_types[7.6] = event_end_dtype_7x
event_end_types[7.7] = event_end_dtype_7x
