from .dtypes import build_dtype, Field


event_end_dtype = build_dtype([
    Field(1, 'event_end', dtype='S4'),
    Field(2, 'event_number'),
    Field(3, 'n_photons_weighted'),
    Field(4, 'n_electrons_weighted'),
    Field(5, 'n_hadrons_weighted'),
    Field(6, 'n_muons_weighted'),
    Field(7, 'n_particles_written'),
    Field(262, 'chi_square_longitudinal'),
    Field(263, 'n_photons_written'),
    Field(264, 'n_electrons_written'),
    Field(265, 'n_hadrons_written'),
    Field(266, 'n_muons_written'),
    Field(267, 'n_em_particles_preshower'),
])
