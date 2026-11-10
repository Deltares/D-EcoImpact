# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""Template-based output for static and single-timestep CGNS results.

Classes:
    CGNSWriter
"""

import os
import shutil
import tempfile
from pathlib import Path

import h5py
import numpy as np
import xarray as xr

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.output_file_settings import OutputFileSettings
from decoimpact.data.entities.cgns_reader import CGNSReader

DATA = " data"

class CGNSWriter:
    """Replace solution variables while leaving the input mesh and time intact."""

    def __init__(self, logger: ILogger):
        self._nodes = CGNSReader(logger)

    def write_file(
        self, dataset: xr.Dataset, path: Path, settings: OutputFileSettings
    ) -> None:
        """Write a validated source template atomically; never modify the source."""
        source = Path(dataset.attrs["cgns_source_path"])
        self._validate_output_not_overwrites_input(source, path)

        with h5py.File(source, "r") as template:
            solution, variables = self._extract_template_data(dataset, template)

        self._write_output_file(dataset, path, source, solution, variables, settings)

    def _validate_output_not_overwrites_input(self, source: Path, path: Path) -> None:
        """Ensure output path does not overwrite input file."""
        if source.resolve() == path.resolve() or (
            path.exists() and os.path.samefile(source, path)
        ):
            raise ValueError("CGNS output must not overwrite the input file.")

    def _extract_template_data(
        self, dataset: xr.Dataset, template: h5py.File
    ) -> tuple:
        """Extract solution node and validated variables from template.
        
        Returns:
            (solution_node, variables_dict)
        """
        zone = template[dataset.attrs["cgns_zone_path"]]
        solution = self._get_solution_node(zone)
        parent = solution if solution is not None else zone
        layouts = self._extract_valid_layouts(parent, solution)
        variables = self._prepare_variables(dataset, layouts, template)
        solution_name = self._get_solution_name(solution, zone)
        self._validate_solution_state(zone, solution, solution_name, variables)
        return solution_name, variables

    def _get_solution_node(self, zone):
        """Get the first FlowSolution_t node or None if none exists."""
        solutions = self._nodes._children(zone, "FlowSolution_t")
        return solutions[0] if solutions else None

    def _extract_valid_layouts(self, parent, solution):
        """Extract valid mesh layouts from parent node."""
        arrays = self._nodes._find_data_arrays(parent)
        return {
            (self._nodes._dims(owner, node[DATA].ndim), node[DATA].shape)
            for owner, node in arrays.values()
            if self._nodes._dims(owner, node[DATA].ndim)
            == self._nodes._dims(parent, node[DATA].ndim)
            and (
                solution is not None
                or self._nodes._label(owner) == "GridCoordinates_t"
            )
        }

    def _get_solution_name(self, solution, zone) -> str:
        """Get the solution node name, using default if not present."""
        if solution is not None:
            return solution.name.rsplit("/", 1)[-1]
        return "EcoImpactSolution"

    def _validate_solution_state(self, zone, solution, solution_name, variables) -> None:
        """Validate that solution state is compatible with output variables."""
        if solution is None and solution_name in zone:
            raise ValueError(f"CGNS node {solution_name} already exists.")
        if solution is not None:
            self._validate_no_metadata_conflicts(solution, variables)

    def _validate_no_metadata_conflicts(self, solution, variables) -> None:
        """Validate that output variables don't conflict with solution metadata."""
        retained_names = {
            child.name.rsplit("/", 1)[-1]
            for child in self._nodes._children(solution)
            if self._nodes._label(child) != "DataArray_t"
        }
        if retained_names.intersection(variables):
            raise ValueError(
                "Output variable conflicts with CGNS solution metadata."
            )

    def _write_output_file(
        self,
        dataset: xr.Dataset,
        path: Path,
        source: Path,
        solution_name: str,
        variables: dict,
        settings: OutputFileSettings,
    ) -> None:
        """Write output file atomically using a temporary file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        handle, temporary = tempfile.mkstemp(suffix=".cgns", dir=path.parent)
        os.close(handle)
        temporary_path = Path(temporary)
        try:
            shutil.copyfile(source, temporary_path)
            with h5py.File(temporary_path, "r+") as output:
                self._update_output_file(output, dataset, solution_name, variables, settings)
            os.replace(temporary_path, path)
        finally:
            temporary_path.unlink(missing_ok=True)

    def _update_output_file(
        self,
        output: h5py.File,
        dataset: xr.Dataset,
        solution_name: str,
        variables: dict,
        settings: OutputFileSettings,
    ) -> None:
        """Update variables and metadata in output file."""
        zone = output[dataset.attrs["cgns_zone_path"]]
        target = self._get_or_create_solution_node(zone, solution_name, output)
        self._delete_existing_arrays(target)
        self._write_variables_and_metadata(target, dataset, variables)
        self._write_provenance(target, settings)

    def _get_or_create_solution_node(self, zone, solution_name, output):
        """Get existing solution node or create new one."""
        if solution_name in zone:
            return zone[solution_name]
        return self._node(zone, solution_name, "FlowSolution_t")

    def _delete_existing_arrays(self, target) -> None:
        """Delete all existing data arrays from target node."""
        for owner, child in self._nodes._find_data_arrays(target).values():
            del owner[child.name.rsplit("/", 1)[-1]]

    def _write_variables_and_metadata(
        self, target, dataset: xr.Dataset, variables: dict
    ) -> None:
        """Write output variables with their attributes."""
        for name, values in variables.items():
            node = self._node(target, name, "DataArray_t", values)
            attributes = dataset[name].attrs
            for key in ("units", "long_name", "description"):
                if key in attributes:
                    self._descriptor(node, key, str(attributes[key]))

    def _write_provenance(self, target, settings: OutputFileSettings) -> None:
        """Write provenance metadata to target node."""
        self._descriptor(
            target,
            "EcoImpactProvenance",
            f"Generated by {settings.application_name} "
            f"{settings.application_version}",
        )

    def _prepare_variables(
        self,
        dataset: xr.Dataset,
        layouts: set[tuple[tuple[str, ...], tuple[int, ...]]],
        template: h5py.File,
    ) -> dict[str, np.ndarray]:
        """Validate output variables and convert them to supported CGNS arrays.

        Variables must have valid CGNS names, match a mesh layout in the
        template, and contain either spatial data or the template's single
        timestep. Boolean, integer, and floating-point values are converted
        to the corresponding supported NumPy dtype.
        """
        variables = {}
        for name, variable in dataset.data_vars.items():
            try:
                encoded = name.encode("ascii")
            except UnicodeEncodeError as exc:
                raise ValueError(f"CGNS variable name must be ASCII: {name!r}") from exc
            if (
                not encoded
                or len(encoded) > 32
                or "/" in name
                or name.startswith(" ")
                or "\x00" in name
                or name in (".", "..", "EcoImpactProvenance")
            ):
                raise ValueError(f"Invalid CGNS variable name: {name!r}")
            if any(dim.startswith("time") and dim != "time" for dim in variable.dims):
                raise ValueError(
                    f"CGNS output does not support derived time axes: {name}"
                )
            if "time" in variable.dims:
                if variable.sizes["time"] != 1:
                    raise ValueError(
                        "CGNS output supports exactly one timestep, not timeseries."
                    )
                if "time" not in variable.coords:
                    raise ValueError(
                        "Single-timestep CGNS output requires its original time value."
                    )
                base = template[dataset.attrs["cgns_base_path"]]
                times = [
                    child[DATA][()].ravel()
                    for iterative in self._nodes._children(base, "BaseIterativeData_t")
                    for child in self._nodes._children(iterative, "DataArray_t")
                    if self._nodes._name(child) == "TimeValues"
                ]
                if not times or not np.array_equal(variable["time"].values, times[0]):
                    raise ValueError(
                        "CGNS output time must match the original TimeValues."
                    )
                variable = variable.isel(time=0, drop=True)
            if (variable.dims, variable.shape) not in layouts:
                raise ValueError(
                    f"CGNS output variable {name!r} has incompatible mesh dimensions "
                    f"{variable.dims} and shape {variable.shape}."
                )
            values = np.asarray(variable.values)
            if values.dtype.kind == "b": # converting boolean to integer
                values = values.astype(np.int32)
            elif values.dtype.kind in "iu": # signed or unsigned integer
                if values.size and (
                    int(values.min()) < np.iinfo(np.int64).min
                    or int(values.max()) > np.iinfo(np.int64).max
                ):
                    raise ValueError(f"CGNS integer values out of range: {name}")
                use_int32 = values.dtype.itemsize <= 4 and (
                    not values.size or values.max() <= np.iinfo(np.int32).max
                )
                values = values.astype(np.int32 if use_int32 else np.int64)
            elif values.dtype.kind == "f" and values.dtype.itemsize <= 8: # floating-point numbers
                values = values.astype(
                    np.float32 if values.dtype.itemsize <= 4 else np.float64
                )
            else:
                raise ValueError(
                    f"Unsupported CGNS output dtype for {name}: {values.dtype}"
                )
            variables[name] = values
        if not variables:
            raise ValueError("CGNS output requires at least one spatial variable.")
        return variables

    @staticmethod
    def _node(parent, name, label, values=None):
        """Create a CGNS node group, its metadata attributes, and optional data.

        When values are provided, they are stored in the CGNS ``" data"``
        dataset and determine the node's CGNS numeric type code.
        """
        node = parent.create_group(name)
        CGNSWriter._string_attribute(node, "name", name, 33)
        CGNSWriter._string_attribute(node, "label", label, 33)
        node.attrs["flags"] = np.array([1], dtype=np.int32)
        type_code = "MT"
        if values is not None:
            type_code = {
                ("i", 1): "C1",
                ("i", 4): "I4",
                ("i", 8): "I8",
                ("f", 4): "R4",
                ("f", 8): "R8",
            }[(values.dtype.kind, values.dtype.itemsize)]
            node.create_dataset(DATA, data=values)
        CGNSWriter._string_attribute(node, "type", type_code, 3)
        return node

    @staticmethod
    def _string_attribute(node, name, value, size):
        """Write an ASCII scalar attribute using CGNS's fixed-width string format.

        The fixed-size NumPy scalar supplies a buffer matching the HDF5 string
        type; its remaining bytes are NUL-padded. This is required for CGNS C
        readers, so writing an untyped byte string directly is not equivalent.
        """
        string_type = h5py.h5t.C_S1.copy()
        string_type.set_size(size)
        string_type.set_strpad(h5py.h5t.STR_NULLTERM)
        attribute = h5py.h5a.create(
            node.id, name.encode("ascii"), string_type, h5py.h5s.create(h5py.h5s.SCALAR)
        )
        try:
            attribute.write(
                np.array(value.encode("ascii"), dtype=f"S{size}"), mtype=string_type
            )
        finally:
            attribute.close()

    def _descriptor(self, parent, name, text):
        """Replace a descriptor node with the UTF-8 encoded text as its data."""
        if name in parent:
            del parent[name]
        self._node(
            parent,
            name,
            "Descriptor_t",
            np.frombuffer(text.encode("utf-8"), dtype=np.int8),
        )
