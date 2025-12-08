import gzip
import secrets
from contextlib import ExitStack
from pathlib import Path

import pytest
import numpy as np

from zstandard import ZstdCompressor

from corsikaio.constants import BLOCK_SIZE_BYTES
from corsikaio.file import CorsikaCherenkovFile
from corsikaio.io import RECORD_MARKER


def test_version():
    from corsikaio import CorsikaFile

    with CorsikaFile('tests/resources/mmcs65') as f:
        assert isinstance(f.version, np.float32)
        assert f.version == np.float32(6.5)

    with CorsikaFile('tests/resources/corsika74100') as f:
        assert isinstance(f.version, np.float32)
        assert f.version == np.float32(7.41)

    with CorsikaFile('tests/resources/corsika76900_thin', thinning = True) as f:
        assert isinstance(f.version, np.float32)
        assert f.version == np.float32(7.69)


def test_next():
    from corsikaio import CorsikaFile

    with CorsikaFile('tests/resources/mmcs65') as f:
        i = 0
        for event in f:
            i += 1
    assert i == 1500

    with CorsikaFile('tests/resources/corsika76900_thin', thinning=True) as f:
        i = 0
        for event in f:
            i += 1
    assert i == 5

def test_cherenkov():

    from corsikaio import CorsikaCherenkovFile

    with CorsikaCherenkovFile('tests/resources/mmcs65', mmcs=True) as f:
        event = next(f)
        assert hasattr(event, 'photons')

    with CorsikaCherenkovFile('tests/resources/cer_corsika76900_thin', thinning=True) as f:
        event = next(f)
        assert hasattr(event, 'photons')


def test_headers():
    from corsikaio import CorsikaCherenkovFile

    with CorsikaCherenkovFile('tests/resources/mmcs65', mmcs=True) as f:
        run_header, event_headers, run_end = f.read_headers()

    assert len(event_headers) == 1500
    assert run_end['n_events'] == 1500

    with CorsikaCherenkovFile('tests/resources/cer_corsika76900_thin', thinning=True) as f:
        run_header, event_headers, run_end = f.read_headers()

    assert len(event_headers) == 200
    assert run_end['n_events'] == 200


def test_accidental_evth():
    from corsikaio import CorsikaCherenkovFile
    with CorsikaCherenkovFile('tests/resources/accidental_evth.gz', mmcs=True) as f:
        run_header, event_headers, run_end = f.read_headers()
        assert len(event_headers) == 1500


def test_run_end():

    from corsikaio import CorsikaCherenkovFile

    with CorsikaCherenkovFile('tests/resources/mmcs65', mmcs=True) as f:
        assert f.run_end['n_events'] == 1500

    with CorsikaCherenkovFile('tests/resources/corsika75700', mmcs=True) as f:
        assert f.run_end['n_events'] == 10

    with CorsikaCherenkovFile('tests/resources/cer_corsika76900_thin', thinning=True) as f:
        assert f.run_end['n_events'] == 200


def test_particle_longi():
    from corsikaio import CorsikaParticleFile

    with CorsikaParticleFile('tests/resources/corsika757_particle') as f:
        assert f.run_end['n_events'] == 10

        for i, e in enumerate(f, start=1):
            assert e.header['event_number'] == i
            assert np.all(e.longitudinal['vertical_depth'] == np.arange(20, 801, 20))


def test_particle_no_parse():
    from corsikaio import CorsikaParticleFile

    with CorsikaParticleFile('tests/resources/corsika757_particle', parse_blocks=False) as f:
        n_read = 0
        for e in f:
            n_read += 1
            # second entry in header is event_number
            assert e.header[1] == n_read
            assert e.header.dtype == np.float32
            assert len(e.header) == 273
            assert e.particles.size % 273 == 0
        assert n_read == 10

    with CorsikaParticleFile('tests/resources/corsika76900_thin', thinning=True, parse_blocks=False) as f:
        n_read = 0
        for e in f:
            n_read += 1
            # second entry in header is event_number
            assert e.header[1] == n_read
            assert e.header.dtype == np.float32
            assert len(e.header) == 312
            assert e.particles.size % 312 == 0
        assert n_read == 5



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

    with open("tests/resources/corsika757_particle", "rb") as f:
        with path.open("wb") as out:
            out.write(f.read(size))

    with pytest.raises(IOError, match="seems to be truncated"):
        with CorsikaParticleFile(path) as f:
            for _ in f:
                pass


def test_longitudinal_parameters():
    '''Test event end blocks contain longitudinal parameters'''
    from corsikaio import CorsikaParticleFile

    path = "tests/resources/corsika_77500_particle"

    with CorsikaParticleFile(path) as f:
        n_events = 0
        for event in f:
            n_events += 1
            assert "longitudinal_fit_parameters" in event.end.dtype.names
            parameters = event.end["longitudinal_fit_parameters"]
            np.testing.assert_array_equal(parameters != 0, True)
        assert n_events == 5


@pytest.mark.parametrize (
    "test_path",
    [
        'tests/resources/mmcs65',
        'tests/resources/corsika74100',
    ]
)
@pytest.mark.parametrize( "compression", ["gz", "zst"])
def test_compressed(test_path, compression, tmp_path):
    from corsikaio import CorsikaCherenkovFile

    test_path = Path(test_path)
    compressed = tmp_path / f"{test_path.name}.{compression}"

    ctx = ExitStack()

    with ctx:
        infile = ctx.enter_context(test_path.open("rb"))
        outfile = ctx.enter_context(compressed.open("wb"))

        if compression == "gz":
            outstream = ctx.enter_context(gzip.GzipFile(fileobj=outfile, mode="wb"))
        elif compression == "zst":
            compressor = ZstdCompressor(level=10)
            outstream = ctx.enter_context(compressor.stream_writer(outfile))
        else:
            raise ValueError(f"Unknown compression: {compression}")

        for chunk in iter(lambda : infile.read(102400), b""):
            outstream.write(chunk)

    with CorsikaCherenkovFile(compressed) as cf, CorsikaCherenkovFile(test_path) as f:
        for event in f:
            compressed_event = next(cf)
            assert event.header["event_number"] == compressed_event.header["event_number"]


def test_eventio(tmp_path):
    from corsikaio.io import MagicBytes
    dummy_eventio = tmp_path / "test.eventio"
    dummy_eventio_zst = tmp_path / "test.eventio.zst"

    dummy_data = secrets.token_bytes(1024)
    payload = MagicBytes.EVENTIO_LE.value + dummy_data
    dummy_eventio.write_bytes(payload)
    comp = ZstdCompressor()
    dummy_eventio_zst.write_bytes(comp.compress(payload))

    with pytest.raises(ValueError, match="eventio"):
        CorsikaCherenkovFile(dummy_eventio)

    with pytest.raises(ValueError, match="eventio"):
        CorsikaCherenkovFile(dummy_eventio_zst)


def test_version_warnings(monkeypatch):
    from corsikaio import CorsikaFile
    from corsikaio import file as corsikaio_file

    monkeypatch.setattr(corsikaio_file, "MIN_VERSION", 7.123)
    monkeypatch.setattr(corsikaio_file, "MAX_VERSION", 7.567)

    with pytest.warns(corsikaio_file.UnknownOldCORSIKA):
        with CorsikaFile('tests/resources/mmcs65') as f:
            assert f.version == np.float32(6.5)

    with pytest.warns(corsikaio_file.UnknownNewCORSIKA):
        with CorsikaFile('tests/resources/corsika76900_thin', thinning = True) as f:
            assert f.version == np.float32(7.69)
