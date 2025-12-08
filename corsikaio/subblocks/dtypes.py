from collections import namedtuple, defaultdict
import numpy as np


Field = namedtuple(
    "Field",
    ["position", "name", "unit", "shape", "dtype", "min_version"],
    defaults=(None, 1, "f4", np.float32(0)),
)


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


def filter_fields_by_version(fields, version):
    """Return only fields whose min_version is <= the provided version."""
    return [field for field in fields if field.min_version <= version]
