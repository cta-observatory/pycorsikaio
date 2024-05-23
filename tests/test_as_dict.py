def test_as_dict():
    from corsikaio import CorsikaCherenkovFile, as_dict

    with CorsikaCherenkovFile('../tests/resources/corsika75700') as f:
        e = next(f)

        header = as_dict(e.header)
        assert isinstance(header, dict)
        assert header['event_number'] == 1
