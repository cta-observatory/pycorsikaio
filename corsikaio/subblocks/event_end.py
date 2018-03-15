import numpy as np


event_end_dtype = np.dtype([
    ('event_end', 'S4'),
    ('event_number', 'float32'),
    ('n_photons_weighted', 'float32'),
    ('n_electrons_weighted', 'float32'),
    ('n_hadrons_weighted', 'float32'),
    ('n_muons_weighted', 'float32'),
    ('n_particles_written', 'float32'),
    ('unused', 'float32', 255),
    ('chi_square_longitudinal', 'float32'),
    ('n_photons_written', 'float32'),
    ('n_electrons_written', 'float32'),
    ('n_hadrons_written', 'float32'),
    ('n_muons_written', 'float32'),
    ('n_em_particles_preshower', 'float32'),
    ('unused2', 'float32', 5),
])
