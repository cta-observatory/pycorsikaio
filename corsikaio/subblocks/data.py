from .dtypes import build_dtype, Field

cherenkov_photons_fields = [
    Field(1, "n_photons", dtype="float32"),
    Field(2, "x", unit="cm", dtype="float32"),
    Field(3, "y", unit="cm", dtype="float32"),
    Field(4, "u", dtype="float32"),
    Field(5, "v", dtype="float32"),
    Field(6, "t", unit="ns", dtype="float32"),
    Field(7, "production_height", unit="cm", dtype="float32"),
]

cherenkov_photons_dtype = build_dtype(cherenkov_photons_fields, itemsize=None)

cherenkov_photons_fields_thin = cherenkov_photons_fields + [
    Field(8, "thinning_level", dtype="float32"),
]

cherenkov_photons_thin_dtype = build_dtype(cherenkov_photons_fields_thin, itemsize=None)

mmcs_cherenkov_photons_fields = [
    Field(1, "n_photons", dtype="float32"),
    Field(2, "x", unit="cm", dtype="float32"),
    Field(3, "y", unit="cm", dtype="float32"),
    Field(4, "u", dtype="float32"),
    Field(5, "v", dtype="float32"),
    Field(6, "t", unit="ns", dtype="float32"),
    Field(7, "wavelength", unit="nm", dtype="float32"),
    Field(8, "mother_particle", dtype="uint16"),
    Field(9, "production_height", unit="cm", dtype="float32"),
]

mmcs_cherenkov_photons_dtype = build_dtype(mmcs_cherenkov_photons_fields, itemsize=None)

particle_data_fields = [
    Field(1, "particle_description", dtype="float32"),
    Field(2, "px", unit="GeV/c", dtype="float32"),
    Field(3, "py", unit="GeV/c", dtype="float32"),
    Field(4, "pz", unit="GeV/c", dtype="float32"),
    Field(5, "x", unit="cm", dtype="float32"),
    Field(6, "y", unit="cm", dtype="float32"),
    Field(7, "t", unit="ns", dtype="float32"),
]

particle_data_dtype = build_dtype(particle_data_fields, itemsize=None)

particle_data_fields_thin = particle_data_fields + [
    Field(8, "thinning_level", dtype="float32"),
]

particle_data_thin_dtype = build_dtype(particle_data_fields_thin, itemsize=None)
