import numpy as np

longitudinal_header_dtype = np.dtype([
    ('LONG', 'S4'),
    ('event_number', 'float32'),
    ('particle_id', 'float32'),
    ('total_energy', 'float32'),
    ('n_longitudinal', 'float32'),
    ('longitudinal_id', 'float32'),
    ('first_interaction_height', 'float32'),
    ('zenith', 'float32'),
    ('azimuth', 'float32'),
    ('energy_cutoff_hadrons', 'float32'),
    ('energy_cutoff_muons', 'float32'),
    ('energy_cutoff_electrons', 'float32'),
    ('energy_cutoff_photons', 'float32'),
])

longitudinal_data_dtype = np.dtype([
    ('vertical_depth', 'float32'),
    ('n_photons', 'float32'),
    ('n_e_plus', 'float32'),
    ('n_e_minus', 'float32'),
    ('n_mu_plus', 'float32'),
    ('n_mu_minus', 'float32'),
    ('n_hadrons', 'float32'),
    ('n_charged', 'float32'),
    ('n_nuclei', 'float32'),
    ('n_cherenkov', 'float32'),
])
