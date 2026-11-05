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
    _create_cgns_file(path)
    return path


def test_read_time_dependent_data_array_with_reference_date(cgns_path):
    """FlowSolutions referenced by FlowSolutionPointers form the time axis"""
    reader = CGNSReader(Mock(ILogger))

    dataset = reader.read_file(cgns_path, ["Pressure"], reference_date="01-01-2010")

    assert list(dataset.data_vars) == ["Pressure"]
    assert dataset["Pressure"].dims == ("time", "cell")
    assert np.array_equal(dataset["Pressure"].values, PRESSURE)
    assert str(dataset["time"].values[1])[:10] == "2010-01-02"


def test_read_time_dependent_data_applies_time_filter(cgns_path):
    reader = CGNSReader(Mock(ILogger))

    dataset = reader.read_file(
        cgns_path,
        ["Pressure"],
        start_date="02-01-2010",
        reference_date="01-01-2010",
    )

    assert np.array_equal(dataset["Pressure"].values, PRESSURE[1:])


def test_read_without_reference_date_keeps_time_values_and_warns(cgns_path):
    logger = Mock(ILogger)
    reader = CGNSReader(logger)

    dataset = reader.read_file(cgns_path, ["Pressure"])

    assert list(dataset["time"].values) == [0.0, 86400.0, 172800.0]
    logger.log_warning.assert_called_once()


def test_read_all_flow_solution_arrays_if_no_variables_given(cgns_path):
    reader = CGNSReader(Mock(ILogger))

    dataset = reader.read_file(cgns_path, [], reference_date="01-01-2010")

    assert sorted(dataset.data_vars) == ["Density", "Pressure"]


def test_read_static_data_array(tmp_path):
    """Without FlowSolutionPointers a single DataArray has no time dimension"""
    path = tmp_path / "static.cgns"
    _create_cgns_file(path, time_dependent=False)
    logger = Mock(ILogger)

    dataset = CGNSReader(logger).read_file(
        path, ["Pressure", "CoordinateX"], start_date="01-01-2010"
    )

    assert dataset["Pressure"].dims == ("cell",)
    assert dataset["CoordinateX"].dims == ("vertex",)
    logger.log_warning.assert_called_once()  # time filter is ignored


def test_read_missing_variable_raises_error_with_available_names(cgns_path):
    reader = CGNSReader(Mock(ILogger))

    with pytest.raises(ValueError) as exc_info:
        reader.read_file(cgns_path, ["Temperature"])

    assert "Temperature" in str(exc_info.value)
    assert "Pressure" in str(exc_info.value)


def test_read_non_existing_file_raises_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        CGNSReader(Mock(ILogger)).read_file(tmp_path / "missing.cgns", ["Pressure"])


def test_data_access_layer_uses_cgns_reader_with_mapping_keys(cgns_path):
    """The mapping keys are the CGNS names, renaming is done by the model"""
    data = DatasetData(
        {
            "filename": str(cgns_path),
            "reference_date": "01-01-2010",
            "variable_mapping": {"Pressure": "q_river"},
        }
    )

    dataset = DataAccessLayer(Mock(ILogger)).read_input_dataset(data)

    assert list(dataset.data_vars) == ["Pressure"]
    assert dataset.sizes["time"] == 3
    assert dataset.attrs["source_format"] == "CGNS"
    rule = Mock()
    rule.name = "pressure rule"
    rule.input_variable_names = ["q_river"]
    rule.output_variable_name = "pressure_level"
    model = RuleBasedModel([dataset], [rule], {"Pressure": "q_river"})

    assert set(model._make_output_variables_list()) == {"time", "Pressure", "q_river"}
    model.initialize(Mock(ILogger))
    assert set(model.output_dataset.data_vars) == {"q_river"}
    assert "time" in model.output_dataset.coords


def test_cgns_step_function_output_can_be_written_to_netcdf(cgns_path, tmp_path):
    logger = Mock(ILogger)
    data_access = DataAccessLayer(logger)
    dataset = CGNSReader(logger).read_file(
        cgns_path, ["Pressure"], reference_date="01-01-2010"
    )
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
    np.testing.assert_array_equal(result.values, [[-5.0, 0.0], [0.0, 0.5], [0.5, 1.0]])
    output_path = tmp_path / "output.nc"
    settings = OutputFileSettings("D-EcoImpact", "0.7.1")
    data_access.write_output_file(model.output_dataset, output_path, settings)

    with _xr.open_dataset(output_path) as written:
        _xr.testing.assert_equal(written["pressure_level"], result)
        _xr.testing.assert_equal(written["time"], dataset["time"])


@pytest.mark.skipif(not EXAMPLE_CGNS.exists(), reason="example.cgns not available")
def test_read_pressure_from_example_file():
    dataset = CGNSReader(Mock(ILogger)).read_file(EXAMPLE_CGNS, ["Pressure"])

    assert "Pressure" in dataset.data_vars
    assert dataset["Pressure"].size > 0
