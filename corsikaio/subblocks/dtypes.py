from collections import namedtuple, defaultdict
import numpy as np


Field = namedtuple('Field', ['position', 'name', 'length', 'dtype'])

# set defaults for dtype and length, this works for the 2 right most attributes
Field.__new__.__defaults__ = (1, 'f4')


def build_dtype(fields):
    dt = defaultdict(list)
    for field in fields:
        dt['names'].append(field.name)
        dt['offsets'].append((field.position - 1) * 4)
        dt['formats'].append((field.dtype, field.length))

    return np.dtype(dict(**dt))
