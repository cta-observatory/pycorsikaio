def test_fortran_raw():
    from corsikaio import is_fortran_raw

    with open('tests/resources/mmcs65', 'rb') as f:
        assert not is_fortran_raw(f)


def test_read_block():
    from corsikaio import is_fortran_raw, read_block

    with open('tests/resources/mmcs65', 'rb') as f:

        fortran_raw = is_fortran_raw(f)
        block = read_block(f, fortran_raw)
        assert block[:4] == b'RUNH'
