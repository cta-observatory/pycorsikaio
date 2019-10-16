from collections import namedtuple, defaultdict
import numpy as np


Field = namedtuple('Field', ['position', 'name', 'shape', 'dtype'])

# set defaults for shape and dtype, this works for the 2 right most attributes
Field.__new__.__defaults__ = (1, 'f4')


def build_dtype(fields, itemsize=4 * 273):
    dt = defaultdict(list)
    dt['itemsize'] = itemsize

    for field in fields:
        dt['names'].append(field.name)
        dt['offsets'].append((field.position - 1) * 4)
        if field.shape != 1:
            dt['formats'].append((field.dtype, field.shape))
        else:
            dt['formats'].append(field.dtype)

    return np.dtype(dict(**dt))
