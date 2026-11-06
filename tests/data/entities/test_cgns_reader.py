# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for CGNSReader class
"""

from pathlib import Path
from unittest.mock import Mock

import h5py
import numpy as np
import pytest
import xarray as _xr

from decoimpact.business.entities.rule_based_model import RuleBasedModel
from decoimpact.business.entities.rules.step_function_rule import StepFunctionRule
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.output_file_settings import OutputFileSettings
from decoimpact.data.entities.cgns_reader import CGNSReader
from decoimpact.data.entities.data_access_layer import DataAccessLayer
from decoimpact.data.entities.dataset_data import DatasetData

EXAMPLE_CGNS = (
    Path(__file__).parents[3] / "tests_acceptance/input_cgns_files/example.cgns"
)
PRESSURE = [[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]


def _node(parent, name, label, data=None):
    """Creates a CGNS node as stored in the CGNS/HDF5 mapping"""
    group = parent.create_group(name)
    group.attrs["name"] = np.bytes_(name)
    group.attrs["label"] = np.bytes_(label)
    group.attrs["type"] = np.bytes_("MT" if data is None else "R8")
    if data is not None:
        group.create_dataset(" data", data=data)
    return group


def _chars(text, width=None):
    text = text if width is None else text.ljust(width)
    return np.frombuffer(text.encode("ascii"), dtype=np.int8)


def _create_cgns_file(path, time_dependent=True):
    """Unstructured zone with 2 cells and Pressure/Density per FlowSolution"""
    with h5py.File(path, "w") as cgns_file:
        base = _node(cgns_file, "Base", "CGNSBase_t", np.array([3, 3]))
        zone = _node(base, "Zone", "Zone_t", np.array([[4, 2, 0]]))
        coordinates = _node(zone, "GridCoordinates", "GridCoordinates_t")
        _node(coordinates, "CoordinateX", "DataArray_t", np.arange(4.0))

        solutions = ["Sol1", "Sol2", "Sol3"] if time_dependent else ["Sol1"]
        for index, solution_name in enumerate(solutions):
            solution = _node(zone, solution_name, "FlowSolution_t")
            _node(solution, "GridLocation", "GridLocation_t", _chars("CellCenter"))
            _node(solution, "Pressure", "DataArray_t", np.array(PRESSURE[index]))
            _node(solution, "Density", "DataArray_t", np.full(2, 1000.0))

        if time_dependent:
            iterative = _node(base, "BaseIterativeData", "BaseIterativeData_t")
            _node(iterative, "TimeValues", "DataArray_t", [0.0, 86400.0, 172800.0])
            zone_iterative = _node(zone, "ZoneIterativeData", "ZoneIterativeData_t")
            pointers = np.stack([_chars(name, 32) for name in solutions])
            _node(zone_iterative, "FlowSolutionPointers", "DataArray_t", pointers)


@pytest.fixture(name="cgns_path")
def fixture_cgns_path(tmp_path):
    path = tmp_path / "test.cgns"
    _create_cgns_file(path, time_dependent=False)
    return path


def test_read_all_flow_solution_arrays_if_no_variables_given(cgns_path):
    reader = CGNSReader(Mock(ILogger))

    dataset = reader.read_file(cgns_path, [])

    assert sorted(dataset.data_vars) == ["Density", "Pressure"]


def test_read_static_data_array(tmp_path):
    """Static CGNS data needs no dates and has no time dimension"""
    path = tmp_path / "static.cgns"
    _create_cgns_file(path, time_dependent=False)
    logger = Mock(ILogger)

    dataset = CGNSReader(logger).read_file(path, ["Pressure"])

    assert dataset["Pressure"].dims == ("cell",)
    np.testing.assert_array_equal(dataset["Pressure"].values, PRESSURE[0])
    assert dataset["Pressure"].attrs["cgns_path"] == "/Base/Zone/Sol1/Pressure"
    logger.log_warning.assert_not_called()


@pytest.mark.parametrize(
    "label",
    ["BaseIterativeData_t", "ZoneIterativeData_t", "both"],
)
@pytest.mark.parametrize("with_solution", [False, True])
def test_single_timestep_is_read_as_static_snapshot(cgns_path, label, with_solution):
    with h5py.File(cgns_path, "a") as cgns_file:
        base = cgns_file["Base"]
        zone = base["Zone"]
        if not with_solution:
            del zone["Sol1"]
        _node(base, "SimulationType", "SimulationType_t", _chars("TimeAccurate"))
        if label in ("BaseIterativeData_t", "both"):
            iterative = _node(base, "BaseIterativeData", "BaseIterativeData_t", [1])
            _node(iterative, "TimeValues", "DataArray_t", [0.0])
        if label in ("ZoneIterativeData_t", "both"):
            iterative = _node(zone, "ZoneIterativeData", "ZoneIterativeData_t")
            pointer = "Sol1" if with_solution else ""
            _node(
                iterative,
                "FlowSolutionPointers",
                "DataArray_t",
                _chars(pointer, 32).reshape(1, 32),
            )

    dataset = DataAccessLayer(Mock(ILogger)).read_input_dataset(
        DatasetData({"filename": str(cgns_path)})
    )

    assert "time" not in dataset.dims
    assert "FlowSolutionPointers" not in dataset
    if with_solution:
        assert sorted(dataset.data_vars) == ["Density", "Pressure"]
        np.testing.assert_array_equal(dataset["Pressure"].values, PRESSURE[0])
    else:
        assert list(dataset.data_vars) == ["CoordinateX"]


@pytest.mark.parametrize(
    "source", ["step_count", "TimeValues", "IterationValues", "pointers"]
)
@pytest.mark.parametrize("count", [0, 2, 3])
def test_invalid_timestep_counts_are_rejected(cgns_path, source, count):
    with h5py.File(cgns_path, "a") as cgns_file:
        base = cgns_file["Base"]
        if source == "pointers":
            iterative = _node(base["Zone"], "ZoneIterativeData", "ZoneIterativeData_t")
            pointers = np.tile(_chars("Sol1", 32), (count, 1))
            _node(iterative, "FlowSolutionPointers", "DataArray_t", pointers)
        else:
            iterative = _node(
                base,
                "BaseIterativeData",
                "BaseIterativeData_t",
                [count if source == "step_count" else 1],
            )
            if source != "step_count":
                _node(iterative, source, "DataArray_t", np.arange(count))

    mock_reader = CGNSReader(Mock(ILogger))
    with pytest.raises(ValueError, match="Exactly one timestep"):
        mock_reader.read_file(cgns_path)


@pytest.mark.parametrize("metadata", ["simulation_type", "base", "zone"])
def test_time_metadata_without_timestep_count_is_rejected(cgns_path, metadata):
    with h5py.File(cgns_path, "a") as cgns_file:
        base = cgns_file["Base"]
        if metadata == "simulation_type":
            _node(base, "SimulationType", "SimulationType_t", _chars("TimeAccurate"))
        elif metadata == "base":
            _node(base, "BaseIterativeData", "BaseIterativeData_t")
        else:
            _node(base["Zone"], "ZoneIterativeData", "ZoneIterativeData_t")

    mock_reader = CGNSReader(Mock(ILogger))
    with pytest.raises(ValueError, match="Cannot determine the timestep count"):
        mock_reader.read_file(cgns_path)


def test_single_time_value_without_declared_count_is_supported(cgns_path):
    with h5py.File(cgns_path, "a") as cgns_file:
        iterative = _node(cgns_file["Base"], "BaseIterativeData", "BaseIterativeData_t")
        _node(iterative, "TimeValues", "DataArray_t", [42.0])

    dataset = CGNSReader(Mock(ILogger)).read_file(cgns_path, ["Pressure"])

    assert dataset["Pressure"].dims == ("cell",)


def test_malformed_solution_pointers_are_rejected(cgns_path):
    with h5py.File(cgns_path, "a") as cgns_file:
        iterative = _node(
            cgns_file["Base/Zone"], "ZoneIterativeData", "ZoneIterativeData_t"
        )
        _node(iterative, "FlowSolutionPointers", "DataArray_t", _chars("Sol1"))

    mock_reader = CGNSReader(Mock(ILogger))
    with pytest.raises(ValueError, match="Invalid FlowSolutionPointers shape"):
        mock_reader.read_file(cgns_path)


def test_explicitly_steady_file_is_supported(cgns_path):
    with h5py.File(cgns_path, "a") as cgns_file:
        _node(
            cgns_file["Base"],
            "SimulationType",
            "SimulationType_t",
            _chars("NonTimeAccurate"),
        )

    dataset = CGNSReader(Mock(ILogger)).read_file(cgns_path, ["Pressure"])

    assert dataset["Pressure"].dims == ("cell",)
    np.testing.assert_array_equal(dataset["Pressure"].values, PRESSURE[0])


@pytest.mark.parametrize("variable_names", [None, [], ["CoordinateX"]])
def test_read_zone_arrays_without_solution(tmp_path, variable_names):
    path = tmp_path / "no_solution.cgns"
    _create_cgns_file(path, time_dependent=False)
    with h5py.File(path, "a") as cgns_file:
        del cgns_file["Base/Zone/Sol1"]

    dataset = CGNSReader(Mock(ILogger)).read_file(path, variable_names)

    assert list(dataset.data_vars) == ["CoordinateX"]
    assert dataset["CoordinateX"].dims == ("vertex",)
    np.testing.assert_array_equal(dataset["CoordinateX"].values, np.arange(4.0))


@pytest.mark.parametrize("with_pointers", [False, True])
@pytest.mark.parametrize("variable_names", [None, ["Pressure"]])
def test_multiple_solutions_raise_before_reading_variables(
    tmp_path, with_pointers, variable_names
):
    path = tmp_path / "multiple_solutions.cgns"
    _create_cgns_file(path)
    with h5py.File(path, "a") as cgns_file:
        zone = cgns_file["Base/Zone"]
        del zone["Sol2/Pressure"]
        del zone["Sol3/Pressure"]
        if not with_pointers:
            del zone["ZoneIterativeData"]

    mock_reader = CGNSReader(Mock(ILogger))
    with pytest.raises(ValueError, match="3 FlowSolution_t nodes"):
        mock_reader.read_file(path, variable_names)


def test_variable_outside_solution_is_not_available(cgns_path):
    mock_reader = CGNSReader(Mock(ILogger))
    with pytest.raises(ValueError, match="CoordinateX.*not found"):
        mock_reader.read_file(cgns_path, ["CoordinateX"])


def test_duplicate_arrays_raise_during_discovery(cgns_path):
    with h5py.File(cgns_path, "a") as cgns_file:
        extra = _node(cgns_file["Base/Zone/Sol1"], "Extra", "UserDefinedData_t")
        _node(extra, "Pressure", "DataArray_t", np.zeros(2))

    mock_reader = CGNSReader(Mock(ILogger))
    with pytest.raises(ValueError, match="DataArray 'Pressure' occurs multiple times"):
        mock_reader.read_file(cgns_path, ["Density"])


def test_read_missing_variable_raises_error_with_available_names(cgns_path):
    reader = CGNSReader(Mock(ILogger))

    with pytest.raises(ValueError) as exc_info:
        reader.read_file(cgns_path, ["Temperature"])

    assert "Temperature" in str(exc_info.value)
    assert "Pressure" in str(exc_info.value)


def test_read_non_existing_file_raises_error(tmp_path):
    reader = CGNSReader(Mock(ILogger))
    with pytest.raises(FileNotFoundError):
        reader.read_file(tmp_path / "missing.cgns", ["Pressure"])


def test_data_access_layer_uses_cgns_reader_with_mapping_keys(cgns_path):
    """The mapping keys are the CGNS names, renaming is done by the model"""
    data = DatasetData(
        {
            "filename": str(cgns_path),
            "variable_mapping": {"Pressure": "q_river"},
        }
    )

    dataset = DataAccessLayer(Mock(ILogger)).read_input_dataset(data)

    assert list(dataset.data_vars) == ["Pressure"]
    assert dataset.sizes["cell"] == 2
    assert dataset.attrs["source_format"] == "CGNS"
    rule = Mock()
    rule.name = "pressure rule"
    rule.input_variable_names = ["q_river"]
    rule.output_variable_name = "pressure_level"
    model = RuleBasedModel([dataset], [rule], {"Pressure": "q_river"})

    assert set(model._make_output_variables_list()) == {"Pressure", "q_river"}
    model.initialize(Mock(ILogger))
    assert set(model.output_dataset.data_vars) == {"q_river"}
    assert "time" not in model.output_dataset.coords


def test_cgns_step_function_output_can_be_written_to_netcdf(cgns_path, tmp_path):
    logger = Mock(ILogger)
    data_access = DataAccessLayer(logger)
    dataset = CGNSReader(logger).read_file(cgns_path, ["Pressure"])
    rule = StepFunctionRule(
        "pressure levels", "pressure", [0.0, 2.0, 4.0, 6.0], [-5.0, 0.0, 0.5, 1.0]
    )
    rule.output_variable_name = "pressure_level"
    model = RuleBasedModel([dataset], [rule], {"Pressure": "pressure"})

    assert model.validate(logger)
    model.initialize(logger)
    model.execute(logger)
    model.finalize(logger)

    result = model.output_dataset["pressure_level"]
    assert "location" not in result.attrs
    assert "mesh" not in result.attrs
    np.testing.assert_array_equal(result.values, [-5.0, 0.0])
    output_path = tmp_path / "output.nc"
    settings = OutputFileSettings("D-EcoImpact", "0.7.1")
    data_access.write_output_file(model.output_dataset, output_path, settings)

    with _xr.open_dataset(output_path) as written:
        _xr.testing.assert_equal(written["pressure_level"], result)


@pytest.mark.skipif(not EXAMPLE_CGNS.exists(), reason="example.cgns not available")
def test_read_pressure_from_example_file():
    dataset = CGNSReader(Mock(ILogger)).read_file(EXAMPLE_CGNS, ["Pressure"])

    assert "Pressure" in dataset.data_vars
    assert dataset["Pressure"].size > 0
