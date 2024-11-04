from .dtypes import build_dtype, Field


run_end_fields = [
    Field(1, "RUNE", dtype="S4"),
    Field(2, "run_number", dtype="float32"),
    Field(3, "n_events", dtype="float32"),
]

run_end_dtype = build_dtype(run_end_fields)
run_end_thin_dtype = build_dtype(run_end_fields, itemsize = 4 * 312)