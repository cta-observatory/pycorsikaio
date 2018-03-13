def test_version():
    from corsikaio.file import CorsikaFile

    with CorsikaFile('tests/resources/mmcs65') as f:
        assert isinstance(f.version, float)
        assert f.version == 6.5

    with CorsikaFile('tests/resources/corsika74100') as f:
        assert isinstance(f.version, float)
        assert f.version == 7.41


def test_iter_event_headers():
    from corsikaio.file import CorsikaFile

    with CorsikaFile('tests/resources/mmcs65') as f:
        event_headers = list(f.iter_event_headers())
        assert len(event_headers) == 1500


def test_next():
    from corsikaio.file import CorsikaFile

    with CorsikaFile('tests/resources/mmcs65') as f:
        i = 0
        for event_header, data_block, event_end in f:
            i += 1
    assert i == 1500
