import pytest

def test_is_not_zstd(tmp_path):
    from corsikaio.io import is_zstd

    path = tmp_path / "no_a_zstd_file"

    with open(path, 'wb') as f:
        f.write(b'Hello World')

    assert not is_zstd(path)

def test_is_zstd(tmp_path):
    zstd = pytest.importorskip("zstandard")

    from corsikaio.io import is_zstd
    path = tmp_path / "zstd_file"

    with open(path, 'wb') as f:
        compressor = zstd.ZstdCompressor()
        with compressor.stream_writer(f) as writer:
            writer.write(b'Hello World')

    assert is_zstd(path)
