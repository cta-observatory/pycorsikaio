from collections import namedtuple, defaultdict
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

