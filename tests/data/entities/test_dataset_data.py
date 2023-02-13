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
        "outputfilename": "output.txt",
        "variable_mapping": {"test": "new"},
    }

    # Act
    data = DatasetData(data_dict)

    # Assert

    assert isinstance(data, IDatasetData)
    assert data.inputpath.endswith("test.yaml")
    assert data.outputpath.endswith("output.txt")
    assert "test" in data.mapping
    assert data.mapping["test"] == "new"


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


def test_dataset_data_write_output_file_should_write_file():
    """When calling write_output_file on a dataset should
    write the specified IDatasetData to an output file
    """

    # Arrange
    # create test set
    # operation_min = OperationType.Min
    data = [1]
    time = pd.date_range("2020-01-01", periods=1)
    dataset = _xr.Dataset(data_vars=dict(data=(["time"], data)), coords=dict(time=time))
    path = get_test_data_path() + "/FlowFM_net.nc"

    output_path = str(get_test_data_path()) + "/results.nc"
    data_dict = {
        "filename": path,
        "outputfilename": output_path,
        "variable_mapping": {"test": "test_new"},
    }
    data = DatasetData(data_dict)

    # Act
    data.write_output_file()

    # Assert
    assert output_path.is_file()


def test_dataset_data_write_output_file_should_check_if_path_exists():
    """When calling write_output_file the provided path
    needs to be checked if it exists"""

    # Arrange
    path = get_test_data_path() + "/FlowFM_net.nc"
    output_path = Path("./non_existing_dir/results.nc")
    data_dict = {
        "filename": path,
        "outputfilename": output_path,
        "variable_mapping": {"test": "test_new"},
    }
    data = DatasetData(data_dict)

    # Act
    with pytest.raises(FileExistsError) as exc_info:
        data.write_output_file()

    exception_raised = exc_info.value

    # Assert
    exc = exception_raised.args[0]
    assert exc.endswith("Make sure the outputfile location is valid.")


def test_dataset_data_write_output_file_should_check_if_extension_is_correct():
    """When calling write_output_file the provided path
    needs to be checked if it exists"""

    # Arrange
    path = get_test_data_path() + "/FlowFM_net.nc"
    output_path = Path(get_test_data_path() + "/NonUgridFile.txt")
    data_dict = {
        "filename": path,
        "outputfilename": output_path,
        "variable_mapping": {"test": "test_new"},
    }
    data = DatasetData(data_dict)

    # Act
    with pytest.raises(NotImplementedError) as exc_info:
        data.write_output_file()

    exception_raised = exc_info.value

    # Assert
    assert exception_raised.args[0].endswith(
        "Currently only UGrid (NetCDF) files are supported."
    )
