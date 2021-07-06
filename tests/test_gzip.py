import gzip


def test_is_not_gzip(tmp_path):
    from corsikaio.io import is_gzip

    path = tmp_path / "no_gzip_file"

    with open(path, 'wb') as f:
        f.write(b'Hello World')

    assert not is_gzip(path)

def test_is_gzip(tmp_path):
    from corsikaio.io import is_gzip

    path = tmp_path / "gzip_file"

    with gzip.open(path, 'wb') as f:
        f.write(b'Hello World')

    assert is_gzip(path)
