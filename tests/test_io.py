import pytest
import numpy as np
from scipy.io import FortranFile

from corsikaio.io import iter_blocks


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


@pytest.fixture()
def simple_dummy_file(tmp_path):
    path = tmp_path / "simple.dat"
    data = bytearray(np.arange(273).astype(np.float32))

    with path.open('wb') as f:
        data[:4] = b'RUNH'
        f.write(data)

        for _ in range(5):
            data[:4] = b'EVTH'
            f.write(data)
            for _ in range(3):
                data[:4] = np.float32(0).tobytes()
                f.write(data)
            data[:4] = b'EVTE'
            f.write(data)
        data[:4] = b'RUNE'
        f.write(data)
    return path


@pytest.fixture()
def fortran_raw_dummy_file(tmp_path):
    path = tmp_path / "fortran_raw.dat"
    data = np.arange(273).astype(np.float32)


    blocks = []
    data[0] = np.frombuffer(b'RUNH', dtype=np.float32)
    blocks.append(data.copy())

    for _ in range(5):
        data[0] = np.frombuffer(b'EVTH', dtype=np.float32)
        blocks.append(data.copy())
        for _ in range(3):
            data[0] = 0.0
            blocks.append(data.copy())
        data[0] = np.frombuffer(b'EVTE', dtype=np.float32)
        blocks.append(data.copy())
    data[0] = np.frombuffer(b'RUNE', dtype=np.float32)
    blocks.append(data.copy())

    blocks_per_record = 5
    with FortranFile(path, mode='w') as f:
        n_records = len(blocks) // blocks_per_record + 1

        for i in range(n_records):
            start = i * blocks_per_record
            stop = (i + 1) * blocks_per_record
            print(start, stop, len(blocks))
            f.write_record(np.concatenate(blocks[start:stop]))

    return path


@pytest.fixture(params=["simple", "fortran_raw"])
def dummy_file(request, fortran_raw_dummy_file, simple_dummy_file):
    if request.param == "simple":
        return simple_dummy_file
    else:
        return fortran_raw_dummy_file


def test_iter_blocks_simple_file(dummy_file):
    """Test for iterblocks for the case of no record markers"""
    data = np.arange(273).astype(np.float32)

    with dummy_file.open('rb') as f:
        block_it = iter_blocks(f)
        block = next(block_it)
        assert block[:4] == b'RUNH'
        assert (np.frombuffer(block[4:], np.float32) == data[1:]).all()

        for _ in range(5):
            block = next(block_it)
            assert block[:4] == b'EVTH'
            assert (np.frombuffer(block[4:], np.float32) == data[1:]).all()
            for _ in range(3):
                block = next(block_it)
                assert (np.frombuffer(block, np.float32) == data).all()
            block = next(block_it)
            assert block[:4] == b'EVTE'
            assert (np.frombuffer(block[4:], np.float32) == data[1:]).all()

        block = next(block_it)
        assert block[:4] == b'RUNE'
        assert (np.frombuffer(block[4:], np.float32) == data[1:]).all()

        with pytest.raises(StopIteration):
            next(block_it)


def test_iter_blocks_all(dummy_file):
    """Test for iterblocks for the case of no record markers"""

    with dummy_file.open('rb') as f:
        n_blocks_read = 0
        for _ in iter_blocks(f):
            n_blocks_read += 1

    assert n_blocks_read == 27

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



@pytest.mark.parametrize("size", (100, 1000, 5000))
def test_iter_blocks_truncated(size, tmp_path, dummy_file):
    path = tmp_path / f"test_truncated_{size}.dat"

    with path.open("wb") as out, dummy_file.open("rb") as infile:
        out.write(infile.read(size))

    with pytest.raises(IOError, match="file seems to be truncated"):
        with path.open("rb") as f:
            for _ in iter_blocks(f):
                pass
