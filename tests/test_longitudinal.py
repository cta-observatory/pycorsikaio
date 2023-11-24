import numpy as np


def test_longitudinal():
    from corsikaio import read_longitudinal_distributions
    path = "./tests/resources/corsika_77500_particle.long"


    n_showers = 0
    for longi in read_longitudinal_distributions(path):
        n_showers += 1
        assert longi["shower"] == n_showers
        assert len(longi["particles"]) == 105
        assert len(longi["energy_deposition"]) == 105
        np.testing.assert_array_equal(np.diff(longi["particles"]["depth"]), 10)
        np.testing.assert_array_equal(np.diff(longi["energy_deposition"]["depth"]), 10)

    assert n_showers == 5

