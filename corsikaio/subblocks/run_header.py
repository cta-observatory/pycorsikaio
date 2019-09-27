from collections import defaultdict
import warnings
from .dtypes import Field, build_dtype


run_header_fields_65 = [
    Field(1, 'run_header', dtype='S4'),
    Field(2, 'run_number'),
    Field(3, 'date'),
    Field(4, 'version'),
    Field(5, 'n_observation_levels'),
    Field(6, 'observation_height', shape=10),
    Field(16, 'energy_spectrum_slope'),
    Field(17, 'energy_min'),
    Field(18, 'energy_max'),
    Field(19, 'egs4_flag'),
    Field(20, 'nkg_flag'),
    Field(21, 'energy_cutoff_hadrons'),
    Field(22, 'energy_cutoff_muons'),
    Field(23, 'energy_cutoff_electrons'),
    Field(24, 'energy_cutoff_photons'),
    Field(25, 'physical_constants_and_interaction_flags', shape=50),
    Field(94 + 1, 'cka', shape=40),
    Field(134 + 1, 'ceta', shape=5),
    Field(139 + 1, 'cstrba', shape=11),
    Field(254 + 1, 'aatm', shape=5),
    Field(259 + 1, 'batm', shape=5),
    Field(264 + 1, 'catm', shape=5),
    Field(270, 'nflain'),
    Field(271, 'nfdif'),
    Field(272, 'nflpi0_100nflpif'),
    Field(273, 'nflche_100nfragm'),
]


# the corsika (up to and including version 7.69) user guide has an error here
# confirmed via mail by T. Pierog. NSHOW is at position 93, not 94 as stated
# in the manual
run_header_fields_7x = [
    Field(1, 'run_header', dtype='S4'),
    Field(2, 'run_number'),
    Field(3, 'date'),
    Field(4, 'version'),
    Field(5, 'n_observation_levels'),
    Field(5 + 1, 'observation_height', shape=10),
    Field(16, 'energy_spectrum_slope'),
    Field(17, 'energy_min'),
    Field(18, 'energy_max'),
    Field(19, 'egs4_flag'),
    Field(20, 'nkg_flag'),
    Field(21, 'energy_cutoff_hadrons'),
    Field(22, 'energy_cutoff_muons'),
    Field(23, 'energy_cutoff_electrons'),
    Field(24, 'energy_cutoff_photons'),
    Field(24 + 1, 'physical_constants_and_interaction_flags', shape=50),
    Field(75, 'inclined_observation_plane_x'),
    Field(76, 'inclined_observation_plane_y'),
    Field(77, 'inclined_observation_plane_z'),
    Field(78, 'inclined_observation_plane_theta'),
    Field(79, 'inclined_observation_plane_phi'),
    Field(93, 'n_showers'),  # Says 94 in the userguide, but it's 93
    Field(94 + 1, 'cka', shape=40),
    Field(134 + 1, 'ceta', shape=5),
    Field(139 + 1, 'cstrba', shape=11),
    Field(248, 'x_scatter'),
    Field(249, 'y_scatter'),
    Field(254 + 1, 'aatm', shape=5),
    Field(259 + 1, 'batm', shape=5),
    Field(264 + 1, 'catm', shape=5),
    Field(270, 'nflain'),
    Field(271, 'nfdif'),
    Field(272, 'nflpi0_100nflpif'),
    Field(273, 'nflche_100nfragm'),
]


run_header_dtype_7x = build_dtype(run_header_fields_7x)
run_header_dtype_65 = build_dtype(run_header_fields_65)


def warn():
    warnings.warn('Version unknown, using run header definition of version 7.x')
    return run_header_dtype_7x


run_header_types = defaultdict(warn)
run_header_types[6.5] = run_header_dtype_65
run_header_types[7.4] = run_header_dtype_7x
run_header_types[7.5] = run_header_dtype_7x
run_header_types[7.6] = run_header_dtype_7x
run_header_types[7.7] = run_header_dtype_7x
