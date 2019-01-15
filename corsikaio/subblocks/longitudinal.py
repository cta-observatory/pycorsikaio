import numpy as np

longitudinal_header_dtype = np.dtype([
    ('LONG', 'S4'),
    ('event_number', 'f4'),
    ('particle_id', 'f4'),
    ('total_energy', 'f4'),
    ('n_longitudinal', 'f4'),
    ('longitudinal_id', 'f4'),
    ('first_interaction_height', 'f4'),
    ('zenith', 'f4'),
    ('azimuth', 'f4'),
    ('energy_cutoff_hadrons', 'f4'),
    ('energy_cutoff_muons', 'f4'),
    ('energy_cutoff_electrons', 'f4'),
    ('energy_cutoff_photons', 'f4'),
])

longitudinal_data_dtype = np.dtype([
    ('vertical_depth', 'f4'),
    ('n_photons', 'f4'),
    ('n_e_plus', 'f4'),
    ('n_e_minus', 'f4'),
    ('n_mu_plus', 'f4'),
    ('n_mu_minus', 'f4'),
    ('n_hadrons', 'f4'),
    ('n_charged', 'f4'),
    ('n_nuclei', 'f4'),
    ('n_cherenkov', 'f4'),
])
