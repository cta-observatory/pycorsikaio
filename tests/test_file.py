def test_version():
    from corsikaio import CorsikaFile

    with CorsikaFile('tests/resources/mmcs65') as f:
        assert isinstance(f.version, float)
        assert f.version == 6.5

    with CorsikaFile('tests/resources/corsika74100') as f:
        assert isinstance(f.version, float)
        assert f.version == 7.41


def test_next():
    from corsikaio import CorsikaFile

    with CorsikaFile('tests/resources/mmcs65') as f:
        i = 0
        for event in f:
            i += 1
    assert i == 1500


def test_cherenkov():

    from corsikaio import CorsikaCherenkovFile

    with CorsikaCherenkovFile('tests/resources/mmcs65', mmcs=True) as f:
        event = next(f)
        assert hasattr(event, 'photons')


def test_headers():
    from corsikaio import CorsikaCherenkovFile

    with CorsikaCherenkovFile('tests/resources/mmcs65', mmcs=True) as f:
        run_header, event_headers, run_end = f.read_headers()


    assert len(event_headers) == 1500
    assert run_end['n_events'] == 1500


def test_accidental_evth():
    from corsikaio import CorsikaCherenkovFile
    with CorsikaCherenkovFile('tests/resources/accidental_evth.gz', mmcs=True) as f:
        run_header, event_headers, run_end = f.read_headers()
        assert len(event_headers) == 1500

