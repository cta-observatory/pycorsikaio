test_files = (
    'tests/resources/mmcs65',
    'tests/resources/corsika75600'
)


def test_fortran_raw():
    from corsikaio import read_buffer_size

    with open('tests/resources/mmcs65', 'rb') as f:
        assert read_buffer_size(f) is None

    with open('tests/resources/corsika75600', 'rb') as f:
        assert read_buffer_size(f) == 22932  # standard CORSIKA buffer size


def test_read_block():
    from corsikaio import read_buffer_size, read_block

    for path in test_files:
        with open(path, 'rb') as f:
            buffer_size = read_buffer_size(f)
            block = read_block(f, buffer_size)
            assert block[:4] == b'RUNH'
