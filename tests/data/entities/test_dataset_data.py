"""
Tests for DatasetData class
"""

from pathlib import Path

import pytest
import xarray as _xr

from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.entities.dataset_data import DatasetData
from tests.testing_utils import get_test_data_path


def test_dataset_data_creation_logic():
    """The DatasetData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Arrange
    data_dict = {
        "filename": "test.yaml",
        "variable_mapping": {"test": "new"},
    }

    # Act
    data = DatasetData(data_dict)

    # Assert

    assert isinstance(data, IDatasetData)
    assert data.inputpath.endswith("test.yaml")
    assert "test" in data.mapping
    assert data.mapping["test"] == "new"


def test_dataset_data_should_contain_system_mapping_after_creation():
    """The DatasetData should contain the system mapping needed
    for visualisation, after creation"""

    # Arrange
    data_dict = {
        "filename": "test.yaml",
        "variable_mapping": {"test": "new"},
    }

    # Act
    data = DatasetData(data_dict)

    # Assert
    assert "mesh2d" in data.mapping
    assert data.mapping["mesh2d"] == "mesh2d"
    assert "mesh2d_face_nodes" in data.mapping
    assert data.mapping["mesh2d_face_nodes"] == "mesh2d_face_nodes"
    assert "mesh2d_edge_nodes" in data.mapping
    assert data.mapping["mesh2d_edge_nodes"] == "mesh2d_edge_nodes"
    assert "mesh2d_face_x_bnd" in data.mapping
    assert data.mapping["mesh2d_face_x_bnd"] == "mesh2d_face_x_bnd"
    assert "mesh2d_face_y_bnd" in data.mapping
    assert data.mapping["mesh2d_face_y_bnd"] == "mesh2d_face_y_bnd"
    assert "mesh2d_face_nodes" in data.mapping
    assert data.mapping["mesh2d_flowelem_bl"] == "mesh2d_flowelem_bl"


def test_dataset_data_get_input_dataset_should_read_file():
    """When calling get_input_dataset on a dataset should
    read the specified IDatasetData.path to create a new DataSet
    """

    # Arrange
    path = get_test_data_path() + "/FlowFM_net.nc"
    data_dict = {
        "filename": path,
        "outputfilename": "output.txt",
        "variable_mapping": {"test": "test_new"},
    }
    data = DatasetData(data_dict)

    # Act
    dataset = data.get_input_dataset()

    # Assert
    assert isinstance(dataset, _xr.Dataset)


def test_dataset_data_get_input_dataset_should_check_if_path_exists():
    """When calling get_input_dataset the provided path
    needs to be checked if it exists"""

    # Arrange
    data_dict = {
        "filename": "non_existing_file.nc",
        "outputfilename": "output.txt",
        "variable_mapping": {"test": "test_new"},
    }
    data = DatasetData(data_dict)

    # Act
    with pytest.raises(FileExistsError) as exc_info:
        data.get_input_dataset()

    exception_raised = exc_info.value

    # Assert
    exc = exception_raised.args[0]
    assert exc.endswith("Make sure the inputfile location is valid.")


def test_dataset_data_get_input_dataset_should_check_if_extension_is_correct():
    """When calling get_input_dataset the provided path
    needs to be checked if it exists"""

    # Arrange
    path = get_test_data_path() + "/NonUgridFile.txt"
    data_dict = {
        "filename": path,
        "outputfilename": "output.txt",
        "variable_mapping": {"test": "test_new"},
    }
    data = DatasetData(data_dict)

    # Act
    with pytest.raises(NotImplementedError) as exc_info:
        data.get_input_dataset()

    exception_raised = exc_info.value

    # Assert
    assert exception_raised.args[0].endswith(
        "Currently only UGrid (NetCDF) files are supported."
    )


def test_dataset_data_get_input_dataset_should_not_read_incorrect_file():
    """When calling get_input_dataset on a dataset should
    read the specified IDatasetData.path. If the file is not correct (not
    readable), raise OSError.
    """

    # Arrange
    path = get_test_data_path() + "/FlowFM_net_incorrect.nc"
    data_dict = {
        "filename": path,
        "outputfilename": "output.txt",
        "variable_mapping": {"test": "test_new"},
    }
    data = DatasetData(data_dict)

    # Act
    with pytest.raises(ValueError) as exc_info:
        data.get_input_dataset()

    exception_raised = exc_info.value
    # Assert

    path = Path(path).resolve()
    assert exception_raised.args[0].endswith(
        f"ERROR: Cannot open input .nc file -- " + str(path)
    )
