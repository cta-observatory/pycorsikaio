from .dtypes import build_dtype, Field


run_end_dtype = build_dtype([
    Field(1, 'RUNE', dtype='S4'),
    Field(2, 'run_number', 'float32'),
    Field(3, 'n_events', 'float32'),
])
