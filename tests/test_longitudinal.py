import pytest
import numpy as np


@pytest.mark.parametrize("slant", (True, False))
def test_longitudinal(slant):
    from corsikaio import read_longitudinal_distributions
    from corsikaio import longitudinal_fit_function

    if slant:
        path = "./tests/resources/corsika_77500_particle_slant.long"
        n_steps = 105
        width = 10
    else:
        path = "./tests/resources/corsika_77500_particle_vertical.long"
        n_steps = 208
        width = 5


    n_showers = 0
    for longi in read_longitudinal_distributions(path):
        n_showers += 1
        assert longi["shower"] == n_showers
        assert longi["slant"] is slant

        assert longi["n_steps"] == n_steps
        assert len(longi["particles"]) == n_steps
        assert len(longi["energy_deposition"]) == n_steps

        np.testing.assert_array_equal(np.diff(longi["particles"]["depth"]), width)
        np.testing.assert_array_equal(np.diff(longi["energy_deposition"]["depth"]), width)

        particles = longi["particles"]


        # can only meaningfully compare hight statistics area
        mask = particles["charged"] > 500
        fit = longitudinal_fit_function(particles["depth"][mask], *longi["parameters"])
        np.testing.assert_allclose(particles["charged"][mask], fit, rtol=0.2)


    if slant:
        assert n_showers == 5
    else:
        assert n_showers == 1


def test_invalid(tmp_path):
    from corsikaio import read_longitudinal_distributions

    with pytest.raises(IOError, match="does not seem to be"):
        next(read_longitudinal_distributions("tests/resources/corsika_77500_particle"))
