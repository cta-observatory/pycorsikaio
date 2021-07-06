test_files = (
    'tests/resources/mmcs65',
    'tests/resources/corsika74100'
)


def test_fortran_raw():
    from corsikaio.io import read_buffer_size

    assert read_buffer_size('tests/resources/mmcs65') is None
    assert read_buffer_size('tests/resources/corsika74100') == 22932  # standard CORSIKA buffer size


def test_fortran_raw_file():
    from corsikaio import CorsikaFile

    events = [e for e in CorsikaFile('tests/resources/corsika75700')]

    assert len(events) == 10


def test_read_block():
    from corsikaio.io import read_buffer_size, read_block

    for path in test_files:
        buffer_size = read_buffer_size(path)
        with open(path, 'rb') as f:
            block = read_block(f, buffer_size)
        assert block[:4] == b'RUNH'


def test_versions():
    from corsikaio.io import read_buffer_size, read_block
    from corsikaio.subblocks import get_version
    from corsikaio.constants import RUNH_VERSION_POSITION
    from corsikaio.constants import EVTH_VERSION_POSITION

    for path, version in zip(test_files, (6.5, 7.41)):
        buffer_size = read_buffer_size(path)

        with open(path, 'rb') as f:
            block = read_block(f, buffer_size)
            assert get_version(block, RUNH_VERSION_POSITION) == version

            block = read_block(f, buffer_size)
            assert get_version(block, EVTH_VERSION_POSITION) == version
