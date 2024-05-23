import pytest
import numpy as np

from corsikaio.constants import BLOCK_SIZE_BYTES
from corsikaio.io import RECORD_MARKER


def test_version():
    from corsikaio import CorsikaFile

    with CorsikaFile('../tests/resources/mmcs65') as f:
        assert isinstance(f.version, float)
        assert f.version == 6.5

    with CorsikaFile('../tests/resources/corsika74100') as f:
        assert isinstance(f.version, float)
        assert f.version == 7.41


def test_next():
    from corsikaio import CorsikaFile

    with CorsikaFile('../tests/resources/mmcs65') as f:
        i = 0
        for event in f:
            i += 1
    assert i == 1500


def test_cherenkov():

    from corsikaio import CorsikaCherenkovFile

    with CorsikaCherenkovFile('../tests/resources/mmcs65', mmcs=True) as f:
        event = next(f)
        assert hasattr(event, 'photons')


def test_headers():
    from corsikaio import CorsikaCherenkovFile

    with CorsikaCherenkovFile('../tests/resources/mmcs65', mmcs=True) as f:
        run_header, event_headers, run_end = f.read_headers()

    assert len(event_headers) == 1500
    assert run_end['n_events'] == 1500


def test_accidental_evth():
    from corsikaio import CorsikaCherenkovFile
    with CorsikaCherenkovFile('../tests/resources/accidental_evth.gz', mmcs=True) as f:
        run_header, event_headers, run_end = f.read_headers()
        assert len(event_headers) == 1500


def test_run_end():

    from corsikaio import CorsikaCherenkovFile

    with CorsikaCherenkovFile('../tests/resources/mmcs65', mmcs=True) as f:
        assert f.run_end['n_events'] == 1500

    with CorsikaCherenkovFile('../tests/resources/corsika75700', mmcs=True) as f:
        assert f.run_end['n_events'] == 10


def test_particle_longi():
    from corsikaio import CorsikaParticleFile

    with CorsikaParticleFile('../tests/resources/corsika757_particle') as f:
        assert f.run_end['n_events'] == 10

        for i, e in enumerate(f, start=1):
            assert e.header['event_number'] == i
            assert np.all(e.longitudinal['vertical_depth'] == np.arange(20, 801, 20))


def test_particle_no_parse():
    from corsikaio import CorsikaParticleFile

    with CorsikaParticleFile('../tests/resources/corsika757_particle', parse_blocks=False) as f:
        n_read = 0
        for e in f:
            n_read += 1
            # second entry in header is event_number
            assert e.header[1] == n_read
            assert e.header.dtype == np.float32
            assert len(e.header) == 273
            assert e.particles.size % 273 == 0
        assert n_read == 10



@pytest.mark.parametrize(
    "size",
    (
        RECORD_MARKER.size + 22932,
        RECORD_MARKER.size + 2 * 22932,
        RECORD_MARKER.size + 3 * 22932,
        2000,
    )
)
def test_truncated(tmp_path, size):
    '''Test we raise a meaningful error for a truncated file

    Truncated files might happen if corsika crashes or the disk is full.

    Regression test for cta-observatory/pycorsikaio#15
    '''
    from corsikaio import CorsikaParticleFile
    path = tmp_path / "truncated.dat"

    with open("../tests/resources/corsika757_particle", "rb") as f:
        with path.open("wb") as out:
            out.write(f.read(size))

    with pytest.raises(IOError, match="seems to be truncated"):
        with CorsikaParticleFile(path) as f:
            for _ in f:
                pass


def test_longitudinal_parameters():
    '''Test event end blocks contain longitudinal parameters'''
    from corsikaio import CorsikaParticleFile

    path = "../tests/resources/corsika_77500_particle"

    with CorsikaParticleFile(path) as f:
        n_events = 0
        for event in f:
            n_events += 1
            assert "longitudinal_fit_parameters" in event.end.dtype.names
            parameters = event.end["longitudinal_fit_parameters"]
            np.testing.assert_array_equal(parameters != 0, True)
        assert n_events == 5
