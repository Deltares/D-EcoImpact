# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for CGNSReader class

Reads CGNS files (CGNS/HDF5) with h5py. In the CGNS/HDF5 mapping every CGNS
node is an HDF5 group with the attributes "name", "label" and "type". The
values of a node are stored in a child dataset named " data".

Classes:
    CGNSReader

"""

from datetime import datetime
from pathlib import Path
from typing import Optional

import h5py
import numpy as np
import pandas as pd
import xarray as _xr

from decoimpact.crosscutting.i_logger import ILogger

_DATA = " data"
_DATE_FORMAT = "%d-%m-%Y"
_LOCATION_DIM_NAMES = {"Vertex": "vertex", "CellCenter": "cell"}


class CGNSReader:
    """Reader that converts DataArray_t nodes of a CGNS file to an xarray Dataset"""

    def __init__(self, logger: ILogger):
        self._logger = logger

    def read_file(
        self,
        path: Path,
        variable_names: Optional[list[str]] = None,
        start_date: str = "None",
        end_date: str = "None",
        reference_date: str = "None",
    ) -> _xr.Dataset:
        """Reads DataArray_t nodes from the first zone of a CGNS file.

        Time dependent data is recognized via the FlowSolutionPointers
        (ZoneIterativeData_t) and TimeValues (BaseIterativeData_t) nodes.

        Args:
            path (Path): path to the .cgns file
            variable_names (list[str], optional): names of the DataArray_t
                nodes to read. If empty, all DataArray_t nodes in the
                FlowSolution_t nodes are read.
            start_date (str): optional start date filter ("DD-MM-YYYY")
            end_date (str): optional end date filter ("DD-MM-YYYY")
            reference_date (str): date ("DD-MM-YYYY") corresponding to time 0
                of the TimeValues (in seconds). Required to create a date
                based time axis.

        Returns:
            _xr.Dataset: dataset with one variable per DataArray_t name

        Raises:
            FileNotFoundError: if the file does not exist
            ValueError: if the file or the requested variables cannot be read
        """
        if not path.exists():
            raise FileNotFoundError(f"ERROR: The CGNS file {path} does not exist.")

        try:
            cgns_file = h5py.File(path, "r")
        except OSError as exc:
            raise ValueError(f"ERROR: Cannot open input .cgns file -- {path}") from exc

        with cgns_file:
            zones = [
                (base, zone)
                for base in self._children(cgns_file, "CGNSBase_t")
                for zone in self._children(base, "Zone_t")
            ]
            if len(zones) == 0:
                raise ValueError(f"ERROR: No Zone_t node found in CGNS file {path}")

            base, zone = zones[0]
            zone_name = self._name(zone)
            if len(zones) > 1:
                self._logger.log_warning(
                    f"CGNS file contains {len(zones)} zones. Only zone "
                    f"'{zone_name}' of base '{self._name(base)}' is read."
                )

            data_arrays = self._find_data_arrays(zone)
            names = variable_names or self._flow_solution_array_names(data_arrays)

            missing = [name for name in names if name not in data_arrays]
            if len(missing) > 0:
                raise ValueError(
                    f"ERROR: Variable(s) {missing} not found as DataArray_t in "
                    f"zone '{zone_name}' of CGNS file {path}. Available "
                    f"DataArray_t nodes: {sorted(data_arrays)}"
                )

            solution_order = self._flow_solution_order(zone)
            data_vars = {}
            for name in names:
                data_vars[name] = self._read_variable(
                    name, data_arrays[name], solution_order
                )
                self._logger.log_info(
                    f"Read CGNS DataArray '{name}' with dimensions "
                    f"{data_vars[name].dims} and shape {data_vars[name].shape}"
                )
            time_values = self._time_values(base)

        dataset = _xr.Dataset(data_vars)
        dataset.attrs["source_format"] = "CGNS"
        dataset = self._add_time_coordinate(dataset, time_values, reference_date)
        return self._apply_time_filter(dataset, start_date, end_date)

    def _find_data_arrays(
        self, group: h5py.Group
    ) -> dict[str, list[tuple[h5py.Group, h5py.Group]]]:
        """Finds all DataArray_t nodes (with their parent node) below a node"""
        found: dict[str, list[tuple[h5py.Group, h5py.Group]]] = {}

        def visit(parent: h5py.Group):
            for child in self._children(parent):
                label = self._label(child)
                if label == "DataArray_t":
                    found.setdefault(self._name(child), []).append((parent, child))
                elif label != "ZoneIterativeData_t":
                    visit(child)

        visit(group)
        return found

    def _flow_solution_array_names(
        self, data_arrays: dict[str, list[tuple[h5py.Group, h5py.Group]]]
    ) -> list[str]:
        return sorted(
            name
            for name, nodes in data_arrays.items()
            if any(self._label(parent) == "FlowSolution_t" for parent, _ in nodes)
        )

    def _flow_solution_order(self, zone: h5py.Group) -> Optional[list[str]]:
        """Names of the FlowSolution_t nodes per time step (FlowSolutionPointers)"""
        for iterative_data in self._children(zone, "ZoneIterativeData_t"):
            pointers = self._child(iterative_data, "FlowSolutionPointers")
            if pointers is not None and _DATA in pointers:
                rows = np.atleast_2d(pointers[_DATA][()])
                return [self._to_string(row) for row in rows]
        return None

    def _time_values(self, base: h5py.Group) -> Optional[np.ndarray]:
        for iterative_data in self._children(base, "BaseIterativeData_t"):
            time_values = self._child(iterative_data, "TimeValues")
            if time_values is not None and _DATA in time_values:
                return np.asarray(time_values[_DATA][()], dtype=float).ravel()
        return None

    def _read_variable(
        self,
        name: str,
        nodes: list[tuple[h5py.Group, h5py.Group]],
        solution_order: Optional[list[str]],
    ) -> _xr.Variable:
        """Reads a DataArray_t, stacking the time steps if it is time dependent"""
        by_solution = {self._name(parent): (parent, node) for parent, node in nodes}
        steps = [s for s in (solution_order or []) if s in by_solution]

        if len(steps) > 0:
            if len(steps) != len(solution_order or []):
                missing_steps = [s for s in solution_order or [] if s not in steps]
                raise ValueError(
                    f"ERROR: DataArray '{name}' is missing in FlowSolution(s) "
                    f"{missing_steps} referenced by FlowSolutionPointers."
                )
            arrays = [by_solution[s][1][_DATA][()] for s in steps]
            if len({array.shape for array in arrays}) > 1:
                raise ValueError(
                    f"ERROR: DataArray '{name}' has different shapes per time step."
                )
            parent, node = by_solution[steps[0]]
            dims = ("time",) + self._dims(parent, arrays[0].ndim)
            return _xr.Variable(dims, np.stack(arrays), {"cgns_path": parent.name})

        if len(nodes) > 1:
            paths = [node.name for _, node in nodes]
            raise ValueError(
                f"ERROR: DataArray '{name}' occurs multiple times ({paths}) and "
                "the CGNS file has no FlowSolutionPointers to order them in time."
            )

        parent, node = nodes[0]
        data = node[_DATA][()]
        return _xr.Variable(
            self._dims(parent, data.ndim), data, {"cgns_path": node.name}
        )

    def _dims(self, parent: h5py.Group, ndim: int) -> tuple[str, ...]:
        """Dimension names based on the GridLocation of the parent node.

        h5py returns CGNS (Fortran ordered) arrays with reversed axes, so a
        structured array has shape (k, j, i).
        """
        location = "Vertex"
        for grid_location in self._children(parent, "GridLocation_t"):
            location = self._read_string(grid_location) or location
        dim_name = _LOCATION_DIM_NAMES.get(location, location.lower())

        if ndim == 1:
            return (dim_name,)
        axes = ["i", "j", "k"][:ndim] if ndim <= 3 else [str(n) for n in range(ndim)]
        return tuple(f"{dim_name}_{axis}" for axis in reversed(axes))

    def _add_time_coordinate(
        self,
        dataset: _xr.Dataset,
        time_values: Optional[np.ndarray],
        reference_date: str,
    ) -> _xr.Dataset:
        if "time" not in dataset.dims:
            return dataset

        n_steps = dataset.sizes["time"]
        if time_values is None or len(time_values) < n_steps:
            raise ValueError(
                "ERROR: CGNS file has FlowSolutionPointers but no (or too few) "
                "TimeValues in BaseIterativeData_t."
            )
        seconds = time_values[:n_steps]

        if reference_date == "None":
            self._logger.log_warning(
                "No reference_date given for the CGNS dataset. The time "
                "coordinate contains the TimeValues (seconds). Add "
                "reference_date to the dataset in the input file to get dates "
                "(needed for time filtering and time based rules)."
            )
            return dataset.assign_coords(time=("time", seconds))

        start = pd.Timestamp(datetime.strptime(reference_date, _DATE_FORMAT))
        times = start + pd.to_timedelta(seconds, unit="s")
        return dataset.assign_coords(time=("time", times))

    def _apply_time_filter(
        self, dataset: _xr.Dataset, start_date: str, end_date: str
    ) -> _xr.Dataset:
        if start_date == "None" and end_date == "None":
            return dataset

        if "time" not in dataset.coords or not np.issubdtype(
            dataset["time"].dtype, np.datetime64
        ):
            self._logger.log_warning(
                "start_date/end_date are ignored: the CGNS dataset has no date "
                "based time axis (requires time dependent data and reference_date)."
            )
            return dataset

        filter_start = (
            datetime.strptime(start_date, _DATE_FORMAT)
            if start_date != "None"
            else None
        )
        filter_end = (
            datetime.strptime(end_date, _DATE_FORMAT) if end_date != "None" else None
        )
        self._logger.log_info(
            f"Applying time filter ({filter_start}, {filter_end}) on dataset"
        )
        return dataset.sel(time=slice(filter_start, filter_end))

    def _children(
        self, group: h5py.Group, label: Optional[str] = None
    ) -> list[h5py.Group]:
        return [
            child
            for child in group.values()
            if isinstance(child, h5py.Group)
            and (label is None or self._label(child) == label)
        ]

    def _child(self, group: h5py.Group, name: str) -> Optional[h5py.Group]:
        for child in self._children(group):
            if self._name(child) == name:
                return child
        return None

    def _label(self, node: h5py.Group) -> str:
        return self._attribute(node, "label")

    def _name(self, node: h5py.Group) -> str:
        return self._attribute(node, "name") or node.name.rsplit("/", 1)[-1]

    def _attribute(self, node: h5py.Group, key: str) -> str:
        value = node.attrs.get(key)
        if value is None:
            return ""
        if isinstance(value, np.ndarray):
            value = value.tobytes()
        if isinstance(value, bytes):
            value = value.decode("ascii", errors="ignore")
        return str(value).strip("\x00 ")

    def _read_string(self, node: h5py.Group) -> str:
        if _DATA not in node:
            return ""
        return self._to_string(node[_DATA][()])

    @staticmethod
    def _to_string(chars: np.ndarray) -> str:
        """Converts a CGNS character array (C1) to a string"""
        raw = np.asarray(chars).astype(np.uint8).ravel().tobytes()
        return raw.decode("ascii", errors="ignore").strip("\x00 ")
