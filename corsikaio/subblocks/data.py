import numpy as np

cherenkov_photons_dtype = np.dtype([
    ('n_photons', 'float32'),
    ('x', 'float32'),
    ('y', 'float32'),
    ('u', 'float32'),
    ('v', 'float32'),
    ('t', 'float32'),
    ('production_height', 'float32'),
])

particle_data_dtype = np.dtype([
    ('particle_description', 'float32'),
    ('px', 'float32'),
    ('py', 'float32'),
    ('pz', 'float32'),
    ('x', 'float32'),
    ('y', 'float32'),
    ('t', 'float32'),
])
