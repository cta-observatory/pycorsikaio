import numpy as np
from collections import defaultdict
import warnings


run_header_dtype_65 = np.dtype([
    ('run_header', 'S4'),  # 1
    ('run_number', 'float32'),  # 2
    ('date', 'float32'),  # 3
    ('version', 'float32'),  # 4
    ('n_observation_levels', 'float32'),  # 5
    ('observation_height', 'float32', (10, )),  # 6 - 15
    ('energy_spectrum_slope', 'float32'),  # 16
    ('energy_min', 'float32'),  # 17
    ('energy_max', 'float32'),  # 18
    ('egs4_flag', 'float32'),  # 19
    ('nkg_flag', 'float32'),  # 20
    ('energy_cutoff_hadrons', 'float32'),  # 21
    ('energy_cutoff_muons', 'float32'),  # 22
    ('energy_cutoff_electrons', 'float32'),  # 23
    ('energy_cutoff_photons', 'float32'),  # 24
    ('physical_constants_and_interaction_flags', 'float32', (50, )),  # 25 - 74
    ('unused', 'float32', (20, )),  # 75 - 94
    ('cka', 'float32', (40, )),  # 95 - 134
    ('ceta', 'float32', (5, )),  # 135 - 139
    ('cstrba', 'float32', (11, )),  # 140 - 150
    ('unused2', 'float32', (104, )),  # 150 - 254
    ('aatm', 'float32', (5, )),  # 255 - 259
    ('batm', 'float32', (5, )),  # 260 - 264
    ('catm', 'float32', (5, )),  # 265 - 269
    ('nflain', 'float32'),  # 270
    ('nfdif', 'float32'),  # 271
    ('nflpi0_100nflpif', 'float32'),  # 272
    ('nflche_100nfgragm', 'float32'),  # 273
])


run_header_dtype_7x = np.dtype([
    ('run_header', 'S4'),  # 1
    ('run_number', 'float32'),  # 2
    ('date', 'float32'),  # 3
    ('version', 'float32'),  # 4
    ('n_observation_levels', 'float32'),  # 5
    ('observation_height', 'float32', (10, )),  # 6 - 15
    ('energy_spectrum_slope', 'float32'),  # 16
    ('energy_min', 'float32'),  # 17
    ('energy_max', 'float32'),  # 18
    ('egs4_flag', 'float32'),  # 19
    ('nkg_flag', 'float32'),  # 20
    ('energy_cutoff_hadrons', 'float32'),  # 21
    ('energy_cutoff_muons', 'float32'),  # 22
    ('energy_cutoff_electrons', 'float32'),  # 23
    ('energy_cutoff_photons', 'float32'),  # 24
    ('physical_constants_and_interaction_flags', 'float32', (50, )), # 24 - 74
    ('inclined_observation_plange_x', 'float32'),  # 75
    ('inclined_observation_plange_y', 'float32'),  # 76
    ('inclined_observation_plange_z', 'float32'),  # 77
    ('inclined_observation_plange_theta', 'float32'),  # 78
    ('inclined_observation_plange_phi', 'float32'),  # 79
    ('unused', 'float32', (14, )),  # 79 - 93
    ('n_showers', 'float32'),  # 94
    ('cka', 'float32', (40, )),
    ('ceta', 'float32', (5, )),
    ('cstrba', 'float32', (11, )),
    ('unused2', 'float32', (97, )),
    ('x_scatter', 'float32'),
    ('y_scatter', 'float32'),
    ('hlay', 'float32', (5, )),
    ('aatm', 'float32', (5, )),
    ('batm', 'float32', (5, )),
    ('catm', 'float32', (5, )),
    ('nflain', 'float32'),
    ('nfdif', 'float32'),
    ('nflpi0_100nflpif', 'float32'),
    ('nflche_100nfgragm', 'float32'),
])


def warn():
    warnings.warn('Version unknown, using run header definition of version 7.6')
    return run_header_dtype_7x


run_header_types = defaultdict(warn)
run_header_types[6.5] = run_header_dtype_65
run_header_types[7.4] = run_header_dtype_7x
run_header_types[7.5] = run_header_dtype_7x
run_header_types[7.6] = run_header_dtype_7x
