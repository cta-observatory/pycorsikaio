# this is adapted from https://github.com/astropy/astropy/blob/master/astropy/version.py
# see https://github.com/astropy/astropy/pull/10774 for a discussion on why this needed.
__all__ = ["__version__"]

try:
    try:
        from ._dev_version import version
    except ImportError:
        from ._version import version
except Exception:
    import warnings

    warnings.warn(
        "Could not determine version; this indicates a broken installation."
        " Install this package from PyPI, using conda, using pip with a git+ url"
        " or from a local git repository."
        " Installing github's autogenerated source release tarballs "
        " does not include version information and should be avoided."
    )
    del warnings
    version = "0.0.0"

__version__ = version
