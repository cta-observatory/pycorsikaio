import numpy as np


run_end_dtype = np.dtype([
    ('RUNE', 'S4'),
    ('run_number', 'float32'),
    ('n_events', 'float32'),
    ('unused', 'float32', 270),
])
