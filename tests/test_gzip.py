import gzip
import tempfile


def test_is_gzip():
    from corsikaio.file import is_gzip

    with tempfile.NamedTemporaryFile() as tmp:
        with open(tmp.name, 'wb') as f:
            f.write(b'Hello World')

        with open(tmp.name, 'rb') as f:
            assert not is_gzip(f)

    with tempfile.NamedTemporaryFile() as tmp:
        with gzip.open(tmp.name, 'wb') as f:
            f.write(b'Hello World')

        with open(tmp.name, 'rb') as f:
            assert is_gzip(f)
