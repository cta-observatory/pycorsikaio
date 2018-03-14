test_files = (
    'tests/resources/mmcs65',
    'tests/resources/corsika74100'
)


def test_fortran_raw():
    from corsikaio import read_buffer_size

    with open('tests/resources/mmcs65', 'rb') as f:
        assert read_buffer_size(f) is None

    with open('tests/resources/corsika74100', 'rb') as f:
        assert read_buffer_size(f) == 22932  # standard CORSIKA buffer size


def test_read_block():
    from corsikaio import read_buffer_size, read_block

    for path in test_files:
        with open(path, 'rb') as f:
            buffer_size = read_buffer_size(f)
            block = read_block(f, buffer_size)
            assert block[:4] == b'RUNH'


def test_versions():
    from corsikaio import read_buffer_size, read_block
    from corsikaio import get_version
    from corsikaio.constants import RUNH_VERSION_POSITION
    from corsikaio.constants import EVTH_VERSION_POSITION

    for path, version in zip(test_files, (6.5, 7.41)):

        with open(path, 'rb') as f:
            buffer_size = read_buffer_size(f)
            block = read_block(f, buffer_size)

            assert get_version(block, RUNH_VERSION_POSITION) == version

            block = read_block(f, buffer_size)

            assert get_version(block, EVTH_VERSION_POSITION) == version


def test_read_headers():
    from corsikaio import read_corsika_headers
    for path, version in zip(test_files, (6.5, 7.41)):
        with open(path, 'rb') as f:
            run_header, event_headers = read_corsika_headers(f)

        assert round(float(run_header['version']), 2) == version
