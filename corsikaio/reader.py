"""Module for parent Reader class.

This class should be used to create new readers for input data
that would result in too complex and heavy functions."""

import logging
from pathlib import Path
import re

try:
    from astropy.table import QTable, join
    from astropy.units import cds
except ModuleNotFoundError as e:
    raise ImportError("You need to install astropy to use this feature") from e

import numpy as np
import numpy.lib.recfunctions as rfn
from corsikaio import CorsikaParticleFile

from .subblocks.run_header import run_header_fields
from .subblocks.event_header import event_header_fields
from .subblocks.data import particle_data_fields, particle_data_dtype
from .subblocks.longitudinal import longitudinal_data_fields
from .subblocks.event_end import event_end_fields
from .subblocks.run_end import run_end_fields

__all__ = ["CorsikaReader"]

logger = logging.getLogger(__name__)


class Reader:
    """Base class for all readers which load data into astropy tables.

    Parameters
    ----------
    input_files: str or pathlib.Path
        Can be,
        - a list of file paths
        - a single file containing a list of paths on disk
        - a regex string like "DAT*"
    recursive: bool
        If True perform regex pattern matching recursively.
        Defaults to False: only the files in the outermost path
        will be considered.
    max_events: int
        Number of events to read from each input file.
        Defaults to None, i.e. all events will be read.
    excluded_keys: list(str)
        List of columns to exclude from the resulting table.
        Defaults to None (no column).
    selected_keys: list(str)
        List of columns to include from the resulting table.
        Defaults to None (all columns).
    """

    def __init__(
        self, input_files, recursive=False, excluded_keys=None, selected_keys=None
    ):
        self.recursive = recursive
        self.input_files = self._initialize_input_files(input_files, self.recursive)
        self.excluded_keys = excluded_keys
        self.selected_keys = selected_keys

    def _initialize_input_files(self, input_files, recursive):
        """Interpret the input as a list of input files.

        Parameters
        ----------
        input_files: str, list(str) or pathlib.Path
            Can be a list of paths, a single path or a regex string.
        recursive: bool
            If True perform regex pattern matching recursively.

        Returns
        -------
        files: list
            List of absolute file paths.
        """

        if isinstance(input_files, list):  # list of files
            files = input_files
        else:
            try:
                if not Path(input_files).exists():
                    re.compile(str(input_files))  # check if it's a valid regex string
                    if recursive:
                        files = [
                            str(f)
                            for f in (Path(input_files).parent).rglob(
                                Path(input_files).name
                            )
                        ]
                    else:
                        files = [
                            str(f)
                            for f in (Path(input_files).parent).glob(
                                Path(input_files).name
                            )
                        ]
                    if len(files) == 0:
                        raise ValueError("No valid input file has been found.")
                else:  # it can be a single file
                    try:  # containing a list of paths
                        with open(
                            Path(input_files).absolute(),
                            "r",
                            encoding="utf-8",
                            newline="\n",
                        ) as f:
                            files = [path.rstrip() for path in f.readlines()]
                            if len(files) == 0:
                                raise EOFError("Input file has no content!")
                    except UnicodeDecodeError:
                        files = [str(Path(input_files).absolute())]
            except re.error:
                raise ValueError("Input is not a valid regex string.")

        return files

    @staticmethod
    def _join_allow_empty(left, right, keys, join_type="left", **kwargs):
        """
        Join two astropy tables, allowing both sides to be empty tables.

        See https://github.com/astropy/astropy/issues/12012 for why
        this is necessary. This behaves as `~astropy.table.join`,
        with the only difference of allowing empty tables to be joined.

        Parameters
        ----------
        left: astropy.table.Table or astropy.table.QTable
        right: astropy.table.Table or astropy.table.QTable
        keys: list(str)
            List of column names to use for joining.
        join_type: str
            Can be on of 'inner', 'outer', 'left' or 'right'.
        **kwargs: dict
            Optional keyword arguments for astropy.table.join.
        """

        left_empty = len(left) == 0
        right_empty = len(right) == 0

        if join_type == "inner":
            if left_empty:
                return left.copy()
            if right_empty:
                return right.copy()

        elif join_type == "left":
            if left_empty or right_empty:
                return left.copy()

        elif join_type == "right":
            if left_empty or right_empty:
                return right.copy()

        elif join_type == "outer":
            if left_empty:
                return right.copy()

            if right_empty:
                return left.copy()

        return join(left, right, keys, join_type=join_type, **kwargs)

    def _join_tables(self, table1, table2, keys=None):
        """Outer join two tables on the keys"""
        # we start with an empty table, but after the first non-empty, we perform
        # left joins
        if len(table1) == 0:
            how = "right"
        else:
            how = "left"
        return self._join_allow_empty(table1, table2, keys=keys, join_type=how)

    @staticmethod
    def _filter_table(table, excluded_keys=None, selected_keys=None, const_keys=None):
        """Filter an astropy table by column name.

        (Q)Table classes provide the keep_columns/remove_columns methods,
        but this function allows to use also sub-strings to remove multiple
        columns in regex-style.

        Parameters
        ----------
        table: astropy.Table
            Input astropy table to reduce.
        excluded_keys: list(str)
            List of columns to exclude from the resulting table.
            Defaults to None (no column).
        selected_keys: list(str)
            List of columns to include from the resulting table.
            Defaults to None (all columns).

        Returns
        -------
        filtered_table: astropy.Table
            Astropy table with less columns.
        """

        if not any([excluded_keys, selected_keys]):
            return table

        const_keys = [] if not const_keys else const_keys

        colnames = table.colnames

        if excluded_keys:
            # remove keys that must be excluded
            filtered_colnames = [
                k
                for k in colnames
                if (all([ex not in k for ex in excluded_keys]) or (k in const_keys))
            ]
        if selected_keys:
            # include only specific keys
            filtered_colnames = [
                k for k in colnames if (any([k in selected_keys]) or (k in const_keys))
            ]
        filtered_table = table[filtered_colnames]
        return filtered_table

    def _refurbish_columns(self, table, leading_cols):
        """Move some columns at the beginning of the table.

        The order of the refurbished columns will be the opposite
        of `self.leading_columns`.

        Parameters
        ----------
        table: astropy.table.Table
            Final (joined) table with selected column names.

        Returns
        -------
        table: astropy.table.Table
            Table with selected columns at the beginning.

        """
        colnames = table.colnames

        for key in leading_cols:
            try:
                colnames.remove(key)
            except ValueError:
                logging.exception("Key %s cannot be removed.", key)
            colnames = [key] + colnames

        return table[colnames]


class CorsikaReader(Reader):
    """Load CORSIKA data into an astropy table.

    Parameters
    ----------
    input_files: str or pathlib.Path
        Can be,

        - a list of file paths
        - a single file containing a list of paths on disk
        - a regex string like "DAT*"

    recursive: bool
        If True perform regex pattern matching recursively.
        Defaults to False: only the files in the outermost path
        will be considered.
    max_events: int
        Number of events to read from each input file.
        Defaults to None, i.e. all events will be read.
    excluded_keys: list(str)
        List of columns to exclude from the resulting table.
        By default, columns with the pure names of the header blocks
        are removed.
    selected_keys: list(str)
        List of columns to include from the resulting table.
        Defaults to None (all columns).

    Returns
    -------
    table: astropy.table.QTable
        Table filled with quantities.
        Run number and event number are always guaranteed to be
        the first two columns.
    """

    def __init__(
        self,
        input_files,
        recursive=False,
        max_events=None,
        excluded_keys=["header", "event_end", "RUNE"],
        selected_keys=None,
        load_run_headers=True,
        load_event_headers=True,
        load_particles=True,
        load_longitudinal=True,
        load_event_ends=False,
        load_run_ends=False,
    ):
        super().__init__(
            input_files=input_files,
            recursive=recursive,
            excluded_keys=excluded_keys,
            selected_keys=selected_keys,
        )

        self.max_events = max_events

        self.load_run_headers = load_run_headers
        self.load_event_headers = load_event_headers
        self.load_particles = load_particles
        self.load_longitudinal = load_longitudinal
        self.load_event_ends = load_event_ends
        self.load_run_ends = load_run_ends

        self.subblock_arrays = {
            "run_headers": [],
            "event_headers": [],
            "particles": [],
            "longitudinal": [],
            "event_ends": [],
            "run_ends": [],
        }

        self.corsika_versions = dict.fromkeys(self.input_files)

    @staticmethod
    def _get_1d_fields(structured_array):
        """Get the set of one dimensional field names in a numpy structured array.

        Parameters
        ----------
        structured_array: np.void

        Returns
        -------
        names: set
        """
        names = []
        for field_name in structured_array.dtype.fields:
            if len(structured_array.dtype.fields[field_name][0].shape) == 0:
                names.append(field_name)
        names = set(names)
        return names

    @staticmethod
    def _stack(list_of_struct_arrays, **opt):
        if len(list_of_struct_arrays) == 1:
            stacked = np.asarray(rfn.stack_arrays(list_of_struct_arrays, **opt))
        else:
            stacked = rfn.stack_arrays(list_of_struct_arrays, **opt)
        return stacked

    def _get_units_from_fields(self, subblock_fields):
        """Retrieve units as a dictionary from the fields of a file subblock.
        Dimensionless fields are not selected.
        Parameters
        ----------
        subblock_fields: list(Field)
            One of the defined lists of fields.
        Return
        ------
        units: dict
            Dictionary with field names as keys and
            string representations of units as values.
        """
        units = {
            field.name: field.unit
            for field in subblock_fields
            if field.unit is not None
        }
        return units

    def _make_table_and_join(
        self, previous_table, previous_joining_keys, subblock_name
    ):

        subblock_arrays_list = self.subblock_arrays[subblock_name]

        # we need to differentiate between 1 and multiple files
        # as single datablocks when stacked don't become ndarrays, but remain np.void
        if len(subblock_arrays_list) > 1:
            subblock = self._stack(subblock_arrays_list, usemask=False)
        elif isinstance(subblock_arrays_list[0], np.void):
            subblock = subblock_arrays_list[0].base
        else:
            subblock = subblock_arrays_list[0]

        subblock_units = self._get_units_from_fields(
            self.subblock_fields[subblock_name]
        )
        table_subblock = QTable(subblock, units=subblock_units)

        joining_keys = (
            previous_joining_keys.intersection(self._get_1d_fields(subblock))
            if len(previous_joining_keys) > 0
            else self._get_1d_fields(subblock)
        )

        if (
            subblock_name not in ["run_headers", "event_headers", "run_ends"]
            and self.load_event_headers
        ):
            joining_keys.add("event_number")

        if not previous_table:
            return table_subblock, joining_keys

        # when joining we need a workaround to preserve row order
        # see https://github.com/astropy/astropy/issues/11619
        table_subblock["__index__"] = np.arange(len(table_subblock))
        table = self._join_tables(previous_table, table_subblock, keys=joining_keys)
        table.sort("__index__")
        del table["__index__"]

        return table, joining_keys

    def _read_file(self, input_file, max_events):
        """Load into memory one Corsika run with Normal Particle Output format.

        The list of subblocks extracted is,
        - run_header
        - event_header
        - particles
        - longitudinal
        - event_end

        Parameters
        ----------
        input_file: str or pathlib.Path
        max_events: int
            Number of simulated shower events to extract from each CORSIKA file

        Returns
        -------
        output : dict
            Nested dictionary with top-level keys 'run_header' and 'event'.
            Each 'event' dictionary is indexed by its event number within the run
            with keys corresponding to the rest of its subblocks.
        """

        with CorsikaParticleFile(input_file) as file:

            run_number = file.run_header[1]
            corsika_version = float(str(file.run_header[3])[:3])
            self.corsika_versions[input_file] = corsika_version

            if not np.all(
                np.array(list(self.corsika_versions.values())) == corsika_version
            ):
                raise ValueError(
                    f"Attempting to read file {input_file} with conflicting Corsika version. Please, check reader.corsika_versions."
                )

            if self.load_run_headers:
                self.subblock_arrays["run_headers"].append(file.run_header)

            if any(
                [
                    self.load_event_headers,
                    self.load_event_ends,
                    self.load_particles,
                    self.load_longitudinal,
                ]
            ):

                for event in file:

                    event_number = event.header[1]

                    if self.load_event_headers:
                        self.subblock_arrays["event_headers"].append(event.header)
                    if self.load_particles:
                        particles = event.particles
                        # if no particles on the ground fill with nans
                        if len(particles) == 0:
                            particles = np.full(
                                shape=(1,), fill_value=np.nan, dtype=particle_data_dtype
                            )
                        # append run_number and event_number
                        # to particles datablock fields
                        particles = rfn.append_fields(
                            particles,
                            [
                                file.run_header.dtype.names[1],
                                event.header.dtype.names[1],
                            ],
                            [
                                [run_number] * len(particles),
                                [event_number] * len(particles),
                            ],
                            dtypes=[
                                file.run_header.dtype["run_number"],
                                event.header.dtype["event_number"],
                            ],
                            usemask=False,
                        )
                        self.subblock_arrays["particles"].append(particles)
                    if self.load_longitudinal:
                        longitudinal = event.longitudinal
                        # append run_number and event_number
                        # to longitudinal datablock fields
                        longitudinal = rfn.append_fields(
                            longitudinal,
                            [
                                file.run_header.dtype.names[1],
                                event.header.dtype.names[1],
                            ],
                            [
                                [run_number] * len(longitudinal),
                                [event_number] * len(longitudinal),
                            ],
                            dtypes=[
                                file.run_header.dtype["run_number"],
                                event.header.dtype["event_number"],
                            ],
                            usemask=False,
                        )
                        self.subblock_arrays["longitudinal"].append(longitudinal)
                    if self.load_event_ends:
                        event_end = event.end
                        event_end = rfn.append_fields(
                            event_end,
                            file.run_header.dtype.names[1],
                            [run_number],
                            dtypes=np.dtype(np.float32),
                            usemask=False,
                        )
                        self.subblock_arrays["event_ends"].append(event_end)

                    if event_number == max_events:
                        break

            if self.load_run_ends:
                self.subblock_arrays["run_ends"].append(file.run_end)

        return corsika_version

    def read(self):
        """Load data into an astropy table from the contructor options.

        Returns
        -------
        table: astropy.table.Table
            Final table with joined fileblocks and selected column names."""

        # cycle on runs
        for i, file in enumerate(self.input_files):

            # cycle on events
            corsika_version = self._read_file(file, self.max_events)

            # get the subblocks fields from the first file
            # self._read_file will raise an exception
            # if a different corsika version is encountered
            if i == 0:
                self.subblock_fields = {
                    "run_headers": run_header_fields[corsika_version],
                    "event_headers": event_header_fields[corsika_version],
                    "particles": particle_data_fields,
                    "longitudinal": longitudinal_data_fields,
                    "event_ends": event_end_fields,
                    "run_ends": run_end_fields,
                }

        table = None
        joining_keys = set()

        with cds.enable():  # this is needed for units like "GeV/c"
            if self.load_run_headers:
                table, joining_keys = self._make_table_and_join(
                    table, joining_keys, "run_headers"
                )
            if self.load_event_headers:
                table, joining_keys = self._make_table_and_join(
                    table, joining_keys, "event_headers"
                )
            if self.load_particles:
                table, joining_keys = self._make_table_and_join(
                    table, joining_keys, "particles"
                )
            if self.load_longitudinal:
                table, joining_keys = self._make_table_and_join(
                    table, joining_keys, "longitudinal"
                )
            if self.load_event_ends:
                table, joining_keys = self._make_table_and_join(
                    table, joining_keys, "event_ends"
                )
            if self.load_run_ends:
                table, joining_keys = self._make_table_and_join(
                    table, joining_keys, "run_ends"
                )

        # Reduce table
        table = self.filter_table(
            table,
            excluded_keys=self.excluded_keys,
            selected_keys=self.selected_keys,
            const_keys=["run_number", "event_number"],
        )

        # refurbish columns so to have run_number and/or event_number
        # always at the beginning of the resulting table
        colnames = table.colnames

        if "run_number" in colnames:
            colnames.remove("run_number")
            colnames = ["run_number"] + colnames

        if "event_number" in colnames:
            colnames.remove("event_number")
            colnames = ["event_number"] + colnames

        return table[colnames]
