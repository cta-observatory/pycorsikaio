import numpy as np


def test_longitudinal():
    from corsikaio import read_longitudinal_distributions
    from corsikaio import longitudinal_fit_function
    path = "./tests/resources/corsika_77500_particle.long"


    n_showers = 0
    for longi in read_longitudinal_distributions(path):
        n_showers += 1
        assert longi["shower"] == n_showers
        assert len(longi["particles"]) == 105
        assert len(longi["energy_deposition"]) == 105
        np.testing.assert_array_equal(np.diff(longi["particles"]["depth"]), 10)
        np.testing.assert_array_equal(np.diff(longi["energy_deposition"]["depth"]), 10)

        particles = longi["particles"]


        # can only meaningfully compare hight statistics area
        mask = particles["charged"] > 500
        fit = longitudinal_fit_function(particles["depth"][mask], *longi["parameters"])
        np.testing.assert_allclose(particles["charged"][mask], fit, rtol=0.2)


    assert n_showers == 5

