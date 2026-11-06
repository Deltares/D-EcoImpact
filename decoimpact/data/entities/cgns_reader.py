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

from pathlib import Path
from typing import Optional

import h5py
import numpy as np
import xarray as _xr

from decoimpact.crosscutting.i_logger import ILogger

_DATA = " data"
_LOCATION_DIM_NAMES = {"Vertex": "vertex", "CellCenter": "cell"}


class CGNSReader:
    """Reader that converts DataArray_t nodes of a CGNS file to an xarray Dataset"""

    def __init__(self, logger: ILogger):
        self._logger = logger

    def read_file(
        self,
        path: Path,
        variable_names: Optional[list[str]] = None,
    ) -> _xr.Dataset:
        """Reads DataArray_t nodes from the first zone of a CGNS file.

        Reads the single FlowSolution_t node, or the zone's DataArray_t
        nodes if no solution exists. Static files and time-dependent files
        with exactly one timestep are read as spatial snapshots, without a
        time dimension. No start or end date is required.

        Args:
            path (Path): path to the .cgns file
            variable_names (list[str], optional): names of the DataArray_t
                nodes to read. If empty, all DataArray_t nodes in the
                selected solution (or zone if no solution exists) are read.

        Returns:
            _xr.Dataset: dataset with one variable per DataArray_t name

        Raises:
            FileNotFoundError: if the file does not exist
            ValueError: if timestep metadata is invalid or indicates multiple
                timesteps, the file contains multiple solutions, or the
                requested variables cannot be read
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

            solutions = self._children(zone, "FlowSolution_t")
            if len(solutions) > 1:
                raise ValueError(
                    f"ERROR: Zone '{zone_name}' in CGNS file {path} contains "
                    f"{len(solutions)} FlowSolution_t nodes. Only one solution "
                    "is supported."
                )
            self._validate_single_timestep(base, zone)
            data_arrays = self._find_data_arrays(solutions[0] if solutions else zone)
            names = variable_names or sorted(data_arrays)

            missing = [name for name in names if name not in data_arrays]
            if len(missing) > 0:
                raise ValueError(
                    f"ERROR: Variable(s) {missing} not found as DataArray_t in "
                    f"zone '{zone_name}' of CGNS file {path}. Available "
                    f"DataArray_t nodes: {sorted(data_arrays)}"
                )

            data_vars = {}
            for name in names:
                data_vars[name] = self._read_variable(*data_arrays[name])
                self._logger.log_info(
                    f"Read CGNS DataArray '{name}' with dimensions "
                    f"{data_vars[name].dims} and shape {data_vars[name].shape}"
                )

        dataset = _xr.Dataset(data_vars)
        dataset.attrs["source_format"] = "CGNS"
        return dataset

    def _validate_single_timestep(self, base: h5py.Group, zone: h5py.Group) -> None:
        """Checks all available timestep counts before treating data as static"""
        base_iterative = self._children(base, "BaseIterativeData_t")
        zone_iterative = self._children(zone, "ZoneIterativeData_t")
        counts = []
        for iterative in base_iterative:
            if _DATA in iterative:
                values = np.asarray(iterative[_DATA][()])
                if values.size != 1 or values.item() != 1:
                    raise ValueError(
                        f"ERROR: Invalid timestep count at '{iterative.name}'. "
                        "Exactly one timestep is supported."
                    )
                counts.append(1)
            for node in self._children(iterative, "DataArray_t"):
                if self._name(node) in ("TimeValues", "IterationValues"):
                    counts.append(node[_DATA].size)

        for iterative in zone_iterative:
            for node in self._children(iterative, "DataArray_t"):
                if self._name(node) == "FlowSolutionPointers":
                    shape = node[_DATA].shape
                    # HDF5 reverses the CGNS (32, NumberOfSteps) axes.
                    if not shape or shape[-1] != 32:
                        raise ValueError(
                            f"ERROR: Invalid FlowSolutionPointers shape {shape} "
                            f"at '{node.name}'. Expected 32 characters per pointer."
                        )
                    counts.append(node[_DATA].size // 32)

        if any(count != 1 for count in counts):
            raise ValueError(
                f"ERROR: Invalid timestep counts {counts} in base "
                f"'{self._name(base)}', zone '{self._name(zone)}'. "
                "Exactly one timestep is supported."
            )
        time_accurate = any(
            self._read_string(node) == "TimeAccurate"
            for node in self._children(base, "SimulationType_t")
        )
        if not counts and (base_iterative or zone_iterative or time_accurate):
            raise ValueError(
                f"ERROR: Cannot determine the timestep count in base "
                f"'{self._name(base)}', zone '{self._name(zone)}'. "
                "Exactly one timestep is required for time-dependent CGNS input."
            )

    def _find_data_arrays(
        self, group: h5py.Group
    ) -> dict[str, tuple[h5py.Group, h5py.Group]]:
        """Finds unique DataArray_t nodes with their parent below a node"""
        found: dict[str, tuple[h5py.Group, h5py.Group]] = {}

        def visit(parent: h5py.Group):
            for child in self._children(parent):
                label = self._label(child)
                if label == "DataArray_t":
                    name = self._name(child)
                    if name in found:
                        raise ValueError(
                            f"ERROR: DataArray '{name}' occurs multiple times "
                            f"({found[name][1].name}, {child.name})."
                        )
                    found[name] = (parent, child)
                elif label != "ZoneIterativeData_t":
                    visit(child)

        visit(group)
        return found

    def _read_variable(self, parent: h5py.Group, node: h5py.Group) -> _xr.Variable:
        """Reads a single DataArray_t"""
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

    def _children(
        self, group: h5py.Group, label: Optional[str] = None
    ) -> list[h5py.Group]:
        return [
            child
            for child in group.values()
            if isinstance(child, h5py.Group)
            and (label is None or self._label(child) == label)
        ]

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
