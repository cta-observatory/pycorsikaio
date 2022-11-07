"""Test the unit attribute of the Field class."""

from corsikaio.subblocks.dtypes import Field
from corsikaio.subblocks import get_units_from_fields

from corsikaio.subblocks.run_header import run_header_fields
from corsikaio.subblocks.event_header import event_header_fields
from corsikaio.subblocks.data import (
    particle_data_fields,
    cherenkov_photons_fields,
    mmcs_cherenkov_photons_fields,
)
from corsikaio.subblocks.longitudinal import (
    longitudinal_data_fields,
    longitudinal_header_fields,
)
from corsikaio.subblocks.event_end import event_end_fields
from corsikaio.subblocks.run_end import run_end_fields


def test_new_field():

    field = Field(1, "test_field")
    assert field.unit == None


def test_event_end_units():

    assert all([f.unit == None for f in event_end_fields])


def test_run_end_units():

    assert all([f.unit == None for f in run_end_fields])


def test_get_units_from_fields():

    test_fields = [
        Field(1, "a"),
        Field(2, "b", unit="cm"),
        Field(3, "c", unit="GeV"),
    ]

    assert get_units_from_fields(test_fields) == {"a": None, "b": "cm", "c": "GeV"}


def test_particle_data_units():

    assert get_units_from_fields(particle_data_fields) == {
        "particle_description": None,
        "px": "Gev/c",
        "py": "Gev/c",
        "pz": "Gev/c",
        "x": "cm",
        "y": "cm",
        "t": "ns",
    }


def test_cherenkov_photons_units():

    assert get_units_from_fields(cherenkov_photons_fields) == {
        "n_photons": None,
        "x": "cm",
        "y": "cm",
        "u": None,
        "v": None,
        "t": "ns",
        "production_height": "cm",
    }


def test_mmcs_cherenkov_photons_units():

    assert get_units_from_fields(mmcs_cherenkov_photons_fields) == {
        "n_photons": None,
        "x": "cm",
        "y": "cm",
        "u": None,
        "v": None,
        "t": "ns",
        "wavelength": "nm",
        "mother_particle": None,
        "production_height": "cm",
    }


def test_longitudinal_header_units():

    assert get_units_from_fields(longitudinal_header_fields) == {
        "LONG": None,
        "event_number": None,
        "particle_id": None,
        "total_energy": "GeV",
        "n_longitudinal": None,
        "longitudinal_id": None,
        "first_interaction_height": "g/cm2",
        "zenith": "rad",
        "azimuth": "rad",
        "energy_cutoff_hadrons": "GeV",
        "energy_cutoff_muons": "GeV",
        "energy_cutoff_electrons": "GeV",
        "energy_cutoff_photons": "GeV",
    }


def test_longitudinal_data_units():

    assert get_units_from_fields(longitudinal_data_fields) == {
        "vertical_depth": "g/cm2",
        "n_photons": None,
        "n_e_plus": None,
        "n_e_minus": None,
        "n_mu_plus": None,
        "n_mu_minus": None,
        "n_hadrons": None,
        "n_charged": None,
        "n_nuclei": None,
        "n_cherenkov": None,
    }
