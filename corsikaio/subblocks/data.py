from .dtypes import build_data_dtype, Field

cherenkov_photons_fields = [
    Field(1, "n_photons", dtype="float32"),
    Field(2, "x", unit="cm", dtype="float32"),
    Field(3, "y", unit="cm", dtype="float32"),
    Field(4, "u", dtype="float32"),
    Field(5, "v", dtype="float32"),
    Field(6, "t", unit="ns", dtype="float32"),
    Field(7, "production_height", unit="cm", dtype="float32"),
]

cherenkov_photons_dtype = build_data_dtype(cherenkov_photons_fields)

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

mmcs_cherenkov_photons_dtype = build_data_dtype(mmcs_cherenkov_photons_fields)

particle_data_fields = [
    Field(1, "particle_description", dtype="float32"),
    Field(2, "px", unit="Gev/c", dtype="float32"),
    Field(3, "py", unit="Gev/c", dtype="float32"),
    Field(4, "pz", unit="Gev/c", dtype="float32"),
    Field(5, "x", unit="cm", dtype="float32"),
    Field(6, "y", unit="cm", dtype="float32"),
    Field(7, "t", unit="ns", dtype="float32"),
]

particle_data_dtype = build_data_dtype(particle_data_fields)
