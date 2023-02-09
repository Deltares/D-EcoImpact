"""
Tests for DatasetData class
"""

import pytest
import xarray as _xr

from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.entities.dataset_data import DatasetData
from tests.testing_utils import get_test_data_path


def test_dataset_data_creation_logic():
    """The DatasetData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Arrange
    data_dict = {"filename": "test.yaml", "variable_mapping": {"test": "new"}}

    # Act
    data = DatasetData(data_dict)

    # Assert

    assert isinstance(data, IDatasetData)
    assert data.path.endswith("test.yaml")
    assert "test" in data.mapping
    assert data.mapping["test"] == "new"


def test_dataset_data_get_input_dataset_should_read_file():
    """When calling get_input_dataset on a dataset should
    read the specified IDatasetData.path to create a new DataSet
    """

    # Arrange
    path = get_test_data_path() + "/FlowFM_net.nc"
    data_dict = {"filename": path, "variable_mapping": {"test": "test_new"}}
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
        "variable_mapping": {"test": "test_new"},
    }
    data = DatasetData(data_dict)

    # Act
    with pytest.raises(FileExistsError) as exc_info:
        data.get_input_dataset()

    exception_raised = exc_info.value

    # Assert
    exc = exception_raised.args[0]
    assert exc.endswith("Make sure the file location is valid.")


def test_dataset_data_get_input_dataset_should_check_if_extension_is_correct():
    """When calling get_input_dataset the provided path
    needs to be checked if it exists"""

    # Arrange
    path = get_test_data_path() + "/NonUgridFile.txt"
    data_dict = {"filename": path, "variable_mapping": {"test": "test_new"}}
    data = DatasetData(data_dict)

    # Act
    with pytest.raises(NotImplementedError) as exc_info:
        data.get_input_dataset()

    exception_raised = exc_info.value

    # Assert
    assert exception_raised.args[0].endswith(
        "Currently only UGrid (NetCDF) files are supported."
    )
