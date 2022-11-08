from .dtypes import Field, build_dtype


longitudinal_header_fields = [
    Field(1, "LONG", shape="S4"),
    Field(2, "event_number", shape="f4"),
    Field(3, "particle_id", shape="f4"),
    Field(4, "total_energy", unit="GeV", shape="f4"),
    Field(5, "n_longitudinal", shape="f4"),
    Field(6, "longitudinal_id", shape="f4"),
    Field(7, "first_interaction_height", unit="g/cm2", shape="f4"),
    Field(8, "zenith", unit="rad", shape="f4"),
    Field(9, "azimuth", unit="rad", shape="f4"),
    Field(10, "energy_cutoff_hadrons", unit="GeV", shape="f4"),
    Field(11, "energy_cutoff_muons", unit="GeV", shape="f4"),
    Field(12, "energy_cutoff_electrons", unit="GeV", shape="f4"),
    Field(13, "energy_cutoff_photons", unit="GeV", shape="f4"),
]

longitudinal_data_fields = [
    Field(1, "vertical_depth", unit="g/cm2", shape="f4"),
    Field(2, "n_photons", shape="f4"),
    Field(3, "n_e_plus", shape="f4"),
    Field(4, "n_e_minus", shape="f4"),
    Field(5, "n_mu_plus", shape="f4"),
    Field(6, "n_mu_minus", shape="f4"),
    Field(7, "n_hadrons", shape="f4"),
    Field(8, "n_charged", shape="f4"),
    Field(9, "n_nuclei", shape="f4"),
    Field(10, "n_cherenkov", shape="f4"),
]

longitudinal_header_dtype = build_dtype(longitudinal_header_fields)
longitudinal_data_dtype = build_dtype(longitudinal_data_fields)
