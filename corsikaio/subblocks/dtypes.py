from collections import namedtuple, defaultdict
import warnings
import numpy as np


Field = namedtuple("Field", ["position", "name", "unit", "shape", "dtype", "min_version"])

# set defaults for unit, shape, dtype and min_version; works for the 4 right most attributes
Field.__new__.__defaults__ = (None, 1, "f4", 0)


def build_dtype(fields, itemsize=4 * 273):
    dt = defaultdict(list)
    if itemsize is not None:
        dt["itemsize"] = itemsize

    for field in fields:
        dt["names"].append(field.name)
        dt["offsets"].append((field.position - 1) * 4)
        if field.shape != 1:
            dt["formats"].append((field.dtype, field.shape))
        else:
            dt["formats"].append(field.dtype)

    return np.dtype(dict(**dt))


def normalize_version(version, fields, subblock_name):
    """Normalize version number and warn if None or too old."""
    min_supported_version = min(field.min_version for field in fields)
    
    if version is None:
        warnings.warn(f"Version unknown, using earliest {subblock_name} definition")
        return min_supported_version
    if version < min_supported_version:
        warnings.warn(
            f"Version {version} older than supported {min_supported_version}; "
            "using earliest definition"
        )
        return min_supported_version
    return version
