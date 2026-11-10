# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""CGNS serialization and source-template preservation tests."""

import shutil
import subprocess
from unittest.mock import Mock, patch

import h5py
import numpy as np
import pytest
import xarray as xr

from decoimpact.business.utils.dataset_utils import merge_list_of_datasets
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.output_file_settings import OutputFileSettings
from decoimpact.data.entities.cgns_reader import CGNSReader
from decoimpact.data.entities.cgns_writer import CGNSWriter
from decoimpact.data.entities.data_access_layer import DataAccessLayer
from decoimpact.data.entities.dataset_data import DatasetData
from tests.data.entities.test_cgns_reader import (
    EXAMPLE_CGNS,
    _chars,
    _create_cgns_file,
    _node,
)


@pytest.fixture
def source_path(tmp_path):
    path = tmp_path / "input.cgns"
    _create_cgns_file(path, time_dependent=False)
    with h5py.File(path, "a") as source:
        _node(source["Base/Zone"], "ZoneType", "ZoneType_t", _chars("Unstructured"))
        elements = _node(source["Base/Zone"], "Elements", "Elements_t", [10, 0])
        _node(elements, "ElementRange", "IndexRange_t", [1, 2])
        _node(elements, "ElementConnectivity", "DataArray_t", [1, 2, 3, 4, 1, 2, 3, 4])
        _node(source, "CGNSLibraryVersion", "CGNSLibraryVersion_t", [4.2])
        for name in ("CoordinateY", "CoordinateZ"):
            _node(
                source["Base/Zone/GridCoordinates"],
                name,
                "DataArray_t",
                np.arange(4.0) * 2,
            )
        _node(source["Base"], "Description", "Descriptor_t", _chars("Mesh metadata"))
    return path


def _snapshot(group):
    result = {}

    def visit(name, node):
        result[name] = (
            dict(node.attrs),
            node[()] if isinstance(node, h5py.Dataset) else None,
        )

    group.visititems(visit)
    return result


def _assert_snapshot_equal(before, after):
    assert before.keys() == after.keys()
    for name, (attributes, data) in before.items():
        other_attributes, other_data = after[name]
        assert attributes.keys() == other_attributes.keys()
        for key, value in attributes.items():
            np.testing.assert_array_equal(value, other_attributes[key])
        np.testing.assert_array_equal(data, other_data)


@pytest.mark.parametrize("timed", [False, True])
def test_preserves_mesh_and_time_and_saves_only_selected_variables(
    source_path, tmp_path, timed
):
    if timed:
        with h5py.File(source_path, "a") as source:
            iterative = _node(
                source["Base"], "BaseIterativeData", "BaseIterativeData_t", [1]
            )
            _node(iterative, "TimeValues", "DataArray_t", [42.0])
            _node(iterative, "IterationValues", "DataArray_t", [7])
            iterative = _node(
                source["Base/Zone"], "ZoneIterativeData", "ZoneIterativeData_t"
            )
            _node(
                iterative,
                "FlowSolutionPointers",
                "DataArray_t",
                _chars("Sol1", 32).reshape(1, 32),
            )
            _node(
                source["Base"],
                "SimulationType",
                "SimulationType_t",
                _chars("TimeAccurate"),
            )
    logger = Mock(ILogger)
    dataset = CGNSReader(logger).read_file(source_path)
    dataset["result"] = dataset["Pressure"] * 3
    dataset["result"].attrs["units"] = "Pa"
    settings = OutputFileSettings("D-EcoImpact", "test")
    settings.variables_to_save = ["result"]
    output_path = tmp_path / "nested" / "output.cgns"
    with h5py.File(source_path, "r") as source:
        before = _snapshot(source)
    DataAccessLayer(logger).write_output_file(dataset, output_path, settings)
    with h5py.File(source_path, "r") as source:
        _assert_snapshot_equal(before, _snapshot(source))
    with h5py.File(source_path, "r") as source, h5py.File(output_path, "r") as output:
        for name in ("Base/Zone/GridCoordinates", "Base/Zone/Elements"):
            _assert_snapshot_equal(_snapshot(source[name]), _snapshot(output[name]))
        np.testing.assert_array_equal(
            source["Base/Zone/ data"][()], output["Base/Zone/ data"][()]
        )
        if timed:
            for name in ("Base/BaseIterativeData", "Base/Zone/ZoneIterativeData"):
                _assert_snapshot_equal(_snapshot(source[name]), _snapshot(output[name]))
        assert output["Base/Zone/Sol1/result"].attrs["type"] == b"R8"
        assert "units" in output["Base/Zone/Sol1/result"]
        assert "Pressure" not in output["Base/Zone/Sol1"]
        assert "Density" not in output["Base/Zone/Sol1"]
        assert "EcoImpactProvenance" in output["Base/Zone/Sol1"]
    written = CGNSReader(logger).read_file(output_path)
    assert set(written.data_vars) == {"result"}
    np.testing.assert_array_equal(written["result"], [3.0, 6.0])


@pytest.mark.parametrize(
    "dimensions,shape,match",
    [
        (("time", "cell"), (2, 2), "timeseries"),
        (("time", "cell"), (0, 2), "one timestep"),
        (("time_year", "cell"), (1, 2), "derived time"),
        (("other",), (2,), "incompatible mesh"),
        (("cell",), (3,), "incompatible mesh"),
    ],
)
def test_rejects_incompatible_results_before_creating_output(
    source_path, tmp_path, dimensions, shape, match
):
    dataset = CGNSReader(Mock(ILogger)).read_file(source_path)[[]]
    # Remove unused input dimensions so the result itself is tested.
    dataset = xr.Dataset(attrs=dataset.attrs)
    dataset["bad"] = xr.DataArray(np.zeros(shape), dims=dimensions)
    output_path = tmp_path / "not_created" / "output.cgns"
    with pytest.raises(ValueError, match=match):
        DataAccessLayer(Mock(ILogger)).write_output_file(
            dataset, output_path, OutputFileSettings("app", "1")
        )
    assert not output_path.parent.exists()


def test_unused_time_coordinate_does_not_turn_static_results_into_timeseries(
    source_path, tmp_path
):
    dataset = CGNSReader(Mock(ILogger)).read_file(source_path)
    dataset = dataset.assign_coords(time=[0, 1, 2])
    output_path = tmp_path / "output.cgns"
    DataAccessLayer(Mock(ILogger)).write_output_file(
        dataset, output_path, OutputFileSettings("app", "1")
    )
    assert "time" not in CGNSReader(Mock(ILogger)).read_file(output_path).dims


@pytest.mark.parametrize(
    "name", ["x" * 33, "a/b", " leading", "nonascii\u00e9", "EcoImpactProvenance"]
)
def test_invalid_generated_names_are_rejected(source_path, tmp_path, name):
    dataset = CGNSReader(Mock(ILogger)).read_file(source_path)
    dataset[name] = dataset["Pressure"]
    with pytest.raises(ValueError, match="name"):
        DataAccessLayer(Mock(ILogger)).write_output_file(
            dataset, tmp_path / "out.cgns", OutputFileSettings("app", "1")
        )


@pytest.mark.parametrize(
    "values,code",
    [
        (np.array([True, False]), b"I4"),
        (np.array([1, 2], dtype=np.int32), b"I4"),
        (np.array([1, 2], dtype=np.int64), b"I8"),
        (np.array([2**32 - 1, 0], dtype=np.uint32), b"I8"),
        (np.array([1, 2], dtype=np.float32), b"R4"),
    ],
)
def test_writes_numeric_types_without_overflow(source_path, tmp_path, values, code):
    dataset = CGNSReader(Mock(ILogger)).read_file(source_path)
    dataset["result"] = ("cell", values)
    output_path = tmp_path / "output.cgns"
    settings = OutputFileSettings("app", "1")
    settings.variables_to_save = ["result"]
    DataAccessLayer(Mock(ILogger)).write_output_file(dataset, output_path, settings)
    with h5py.File(output_path, "r") as output:
        assert output["Base/Zone/Sol1/result"].attrs["type"] == code
        np.testing.assert_array_equal(output["Base/Zone/Sol1/result/ data"], values)


def test_rejects_unsupported_dtype(source_path, tmp_path):
    dataset = CGNSReader(Mock(ILogger)).read_file(source_path)
    dataset["result"] = ("cell", ["a", "b"])
    with pytest.raises(ValueError, match="dtype"):
        DataAccessLayer(Mock(ILogger)).write_output_file(
            dataset, tmp_path / "output.cgns", OutputFileSettings("app", "1")
        )


def test_input_cannot_be_overwritten(source_path):
    original = source_path.read_bytes()
    dataset = CGNSReader(Mock(ILogger)).read_file(source_path)
    with pytest.raises(ValueError, match="overwrite"):
        DataAccessLayer(Mock(ILogger)).write_output_file(
            dataset, source_path, OutputFileSettings("app", "1")
        )
    assert source_path.read_bytes() == original


def test_failed_write_preserves_existing_destination_and_cleans_temporary_file(
    source_path, tmp_path
):
    dataset = CGNSReader(Mock(ILogger)).read_file(source_path)
    output_path = tmp_path / "output.cgns"
    output_path.write_bytes(b"existing destination")
    with patch(
        "decoimpact.data.entities.cgns_writer.os.replace",
        side_effect=OSError("write failed"),
    ):
        with pytest.raises(OSError, match="write failed"):
            DataAccessLayer(Mock(ILogger)).write_output_file(
                dataset, output_path, OutputFileSettings("app", "1")
            )
    assert output_path.read_bytes() == b"existing destination"
    assert set(tmp_path.glob("*.cgns")) == {source_path, output_path}


def test_mixed_or_conflicting_source_templates_are_rejected(source_path):
    dataset = CGNSReader(Mock(ILogger)).read_file(source_path)
    with pytest.raises(ValueError, match="templates/formats"):
        merge_list_of_datasets([dataset, xr.Dataset()])
    other = dataset.copy()
    other.attrs["cgns_source_path"] = "different.cgns"
    with pytest.raises(ValueError, match="templates/formats"):
        merge_list_of_datasets([dataset, other])


@pytest.mark.parametrize("cgns_input", [False, True])
def test_cannot_convert_formats(source_path, tmp_path, cgns_input):
    dataset = (
        CGNSReader(Mock(ILogger)).read_file(source_path) if cgns_input else xr.Dataset()
    )
    output_path = tmp_path / "new" / ("output.nc" if cgns_input else "output.cgns")
    with pytest.raises(ValueError):
        DataAccessLayer(Mock(ILogger)).write_output_file(
            dataset, output_path, OutputFileSettings("app", "1")
        )
    assert not output_path.parent.exists()


def test_missing_source_provenance_is_rejected(tmp_path):
    dataset = xr.Dataset(attrs={"source_format": "CGNS"})
    with pytest.raises(ValueError, match="provenance"):
        DataAccessLayer(Mock(ILogger)).write_output_file(
            dataset, tmp_path / "out.cgns", OutputFileSettings("app", "1")
        )


@pytest.mark.parametrize("location,shape", [("Vertex", (4,)), ("CellCenter", (2, 3))])
def test_vertex_and_structured_axis_order_are_preserved(
    source_path, tmp_path, location, shape
):
    values = np.arange(np.prod(shape), dtype=np.float64).reshape(shape)
    with h5py.File(source_path, "a") as source:
        solution = source["Base/Zone/Sol1"]
        del solution["GridLocation"]
        _node(solution, "GridLocation", "GridLocation_t", _chars(location))
        for name in ("Pressure", "Density"):
            del solution[name]
        _node(solution, "Pressure", "DataArray_t", values)
        if len(shape) == 2:
            del source["Base/Zone/ data"]
            source["Base/Zone"].create_dataset(
                " data", data=np.array([[4, 3], [3, 2], [0, 0]], dtype=np.int32)
            )
            del source["Base/Zone/ZoneType"]
            _node(source["Base/Zone"], "ZoneType", "ZoneType_t", _chars("Structured"))
    dataset = CGNSReader(Mock(ILogger)).read_file(source_path)
    dataset["result"] = dataset["Pressure"] + 1
    output_path = tmp_path / "output.cgns"
    settings = OutputFileSettings("app", "1")
    settings.variables_to_save = ["result"]
    DataAccessLayer(Mock(ILogger)).write_output_file(dataset, output_path, settings)
    written = CGNSReader(Mock(ILogger)).read_file(output_path)
    assert written["result"].dims == dataset["Pressure"].dims
    np.testing.assert_array_equal(written["result"], values + 1)


@pytest.mark.parametrize("time_value,accepted", [(42.0, True), (43.0, False)])
def test_single_explicit_timestep_must_match_original_time(
    source_path, tmp_path, time_value, accepted
):
    with h5py.File(source_path, "a") as source:
        iterative = _node(
            source["Base"], "BaseIterativeData", "BaseIterativeData_t", [1]
        )
        _node(iterative, "TimeValues", "DataArray_t", [42.0])
    dataset = CGNSReader(Mock(ILogger)).read_file(source_path)
    dataset["result"] = dataset["Pressure"].expand_dims(time=[time_value])
    output_path = tmp_path / "output.cgns"
    settings = OutputFileSettings("app", "1")
    settings.variables_to_save = ["result"]
    if accepted:
        DataAccessLayer(Mock(ILogger)).write_output_file(dataset, output_path, settings)
        np.testing.assert_array_equal(
            CGNSReader(Mock(ILogger)).read_file(output_path)["result"], [1.0, 2.0]
        )
    else:
        with pytest.raises(ValueError, match="TimeValues"):
            DataAccessLayer(Mock(ILogger)).write_output_file(
                dataset, output_path, settings
            )
        assert not output_path.exists()


def test_output_source_must_match_provenance(source_path, tmp_path):
    dataset = CGNSReader(Mock(ILogger)).read_file(source_path)
    settings = OutputFileSettings("app", "1")
    settings.source_path = tmp_path / "different.cgns"
    with pytest.raises(ValueError, match="provenance"):
        DataAccessLayer(Mock(ILogger)).write_output_file(
            dataset, tmp_path / "out.cgns", settings
        )


def test_missing_selected_variable_is_reported(source_path, tmp_path):
    dataset = CGNSReader(Mock(ILogger)).read_file(source_path)
    settings = OutputFileSettings("app", "1")
    settings.variables_to_save = ["missing"]
    with pytest.raises(OSError, match="missing"):
        DataAccessLayer(Mock(ILogger)).write_output_file(
            dataset, tmp_path / "out.cgns", settings
        )


def test_missing_source_file_is_reported(source_path, tmp_path):
    dataset = CGNSReader(Mock(ILogger)).read_file(source_path)
    source_path.unlink()
    with pytest.raises(OSError):
        DataAccessLayer(Mock(ILogger)).write_output_file(
            dataset, tmp_path / "out.cgns", OutputFileSettings("app", "1")
        )


def test_uint64_overflow_is_rejected(source_path, tmp_path):
    dataset = CGNSReader(Mock(ILogger)).read_file(source_path)
    dataset["overflow"] = ("cell", np.array([2**64 - 1, 0], dtype=np.uint64))
    with pytest.raises(ValueError, match="out of range"):
        DataAccessLayer(Mock(ILogger)).write_output_file(
            dataset, tmp_path / "out.cgns", OutputFileSettings("app", "1")
        )


def test_zone_without_solution_gets_vertex_solution(source_path, tmp_path):
    with h5py.File(source_path, "a") as source:
        del source["Base/Zone/Sol1"]
    dataset = CGNSReader(Mock(ILogger)).read_file(source_path, ["CoordinateX"])
    dataset["result"] = dataset["CoordinateX"] + 2
    settings = OutputFileSettings("app", "1")
    settings.variables_to_save = ["result"]
    output_path = tmp_path / "output.cgns"
    DataAccessLayer(Mock(ILogger)).write_output_file(dataset, output_path, settings)
    written = CGNSReader(Mock(ILogger)).read_file(output_path)
    assert written["result"].dims == ("vertex",)
    np.testing.assert_array_equal(written["result"], np.arange(4.0) + 2)


def test_netcdf_input_format_is_not_inferred_from_stale_file_attributes(tmp_path):
    source_path = tmp_path / "input.nc"
    xr.Dataset(
        {"value": ("cell", [1.0, 2.0])}, attrs={"source_format": "CGNS"}
    ).to_netcdf(source_path)
    layer = DataAccessLayer(Mock(ILogger))
    dataset = layer.read_input_dataset(DatasetData({"filename": str(source_path)}))
    try:
        assert dataset.attrs["source_format"] == "NetCDF"
        layer.write_output_file(
            dataset, tmp_path / "output.nc", OutputFileSettings("app", "1")
        )
        with pytest.raises(ValueError):
            layer.write_output_file(
                dataset, tmp_path / "output.cgns", OutputFileSettings("app", "1")
            )
    finally:
        dataset.close()


@pytest.mark.skipif(not EXAMPLE_CGNS.exists(), reason="example.cgns not available")
def test_writes_results_using_real_cgns_example(tmp_path):
    logger = Mock(ILogger)
    dataset = CGNSReader(logger).read_file(EXAMPLE_CGNS, ["Pressure"])
    dataset["result"] = dataset["Pressure"] * 2
    output_path = tmp_path / "output.cgns"
    settings = OutputFileSettings("app", "1")
    settings.variables_to_save = ["result"]
    DataAccessLayer(logger).write_output_file(dataset, output_path, settings)
    written = CGNSReader(logger).read_file(output_path)
    assert set(written.data_vars) == {"result"}
    np.testing.assert_array_equal(written["result"], dataset["result"])


@pytest.mark.parametrize("name", ["x", "fast_or_not", "x" * 32])
def test_generated_attributes_use_cgns_fixed_width_null_terminated_strings(
    tmp_path, name
):
    with h5py.File(tmp_path / "attributes.h5", "w") as output:
        node = CGNSWriter._node(
            output, name, "DataArray_t", np.array([1.0], dtype=np.float64)
        )
        for key, value, size in [
            ("name", name, 33),
            ("label", "DataArray_t", 33),
            ("type", "R8", 3),
        ]:
            attribute_type = node.attrs.get_id(key).get_type()
            assert attribute_type.get_size() == size
            assert attribute_type.get_strpad() == h5py.h5t.STR_NULLTERM
            assert node.attrs[key] == value.encode("ascii")
            raw = np.empty((), dtype=f"S{size}")
            node.attrs.get_id(key).read(raw, mtype=attribute_type)
            assert raw.tobytes() == value.encode("ascii").ljust(size, b"\x00")
