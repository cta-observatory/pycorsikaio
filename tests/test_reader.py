"""Tests for the CorsikaReader."""

from astropy.table import Table
import pytest
from corsikaio.reader import CorsikaReader


def create_test_file(indir, name="test_file", fmt=".txt"):

    path = indir / "".join([name, fmt])
    path.touch()

    return path


@pytest.fixture(scope="session")
def testing_data_path(tmp_path_factory):
    """Temporary directory for global test data"""
    return tmp_path_factory.mktemp("testing_data")


@pytest.fixture
def empty_test_file(testing_data_path):

    p = create_test_file(testing_data_path, name="empty_test_file", fmt=".txt")
    return p


@pytest.fixture
def nested_test_file(testing_data_path):
    """Test file in nested directory"""

    nested_dir = testing_data_path / "subdir"
    nested_dir.mkdir()

    p = create_test_file(nested_dir, name="nested_test_file", fmt=".txt")
    return p


@pytest.fixture
def list_test_file(testing_data_path):
    """Test file in nested directory"""

    p = create_test_file(testing_data_path, name="list_test_file", fmt=".txt")
    with open(p, "a") as f:
        f.write("/some/path\n")
        f.write("/some/other/path")

    return p


def test_Reader_nonexistent_file(testing_data_path):

    with pytest.raises(ValueError, match="No valid input file has been found."):
        CorsikaReader(testing_data_path / "bla.txt")


def test_Reader_input_single_empty_file(empty_test_file):

    with pytest.raises(EOFError, match="Input file has no content!"):
        CorsikaReader(empty_test_file)


def test_CorsikaReader_input_file_with_list(list_test_file):

    r = CorsikaReader(list_test_file)
    assert r.input_files == ["/some/path", "/some/other/path"]


def test_CorsikaReader_input_regex(testing_data_path, empty_test_file, list_test_file):

    r = CorsikaReader(testing_data_path / "*test_file.txt")
    assert str(empty_test_file) in r.input_files
    assert str(list_test_file) in r.input_files


def test_Reader_input_regex_recursive(
    testing_data_path, empty_test_file, list_test_file, nested_test_file
):

    r = CorsikaReader(testing_data_path / "*test_file.txt", recursive=True)
    assert str(empty_test_file) in r.input_files
    assert str(list_test_file) in r.input_files
    assert str(nested_test_file) in r.input_files


def test_CorsikaReader_filter_table(list_test_file):

    r = CorsikaReader(list_test_file)

    b = [2.0, 5.0, 8.5]
    c = ["x", "y", "z"]
    d = ["x", "y", "z"]
    table = Table([b, c, d], names=("b", "c", "d"))

    new_table = r._filter_table(table, excluded_keys=["c"])
    assert new_table.colnames == ["b", "d"]

    new_table = r._filter_table(table, selected_keys=["c"])
    assert new_table.colnames == ["c"]

    new_table = r._filter_table(table)
    assert new_table.colnames == table.colnames

    new_table = r._filter_table(table, selected_keys=["c"], const_keys=["d"])
    assert new_table.colnames == ["c", "d"]
