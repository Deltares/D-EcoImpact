# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the 
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for DataAccessLayer class
"""

from datetime import datetime
from pathlib import Path
from unittest.mock import Mock

import pandas as pd
import pytest
import xarray as _xr

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.crosscutting.logger_factory import LoggerFactory
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.entities.data_access_layer import DataAccessLayer
from decoimpact.data.entities.dataset_data import DatasetData
from decoimpact.data.entities.yaml_model_data import YamlModelData
from tests.testing_utils import get_test_data_path


def test_input_version():
    """The DataAccessLayer should read the version from the input.yaml"""

    # Arrange
    logger = LoggerFactory.create_logger()
    path = Path(get_test_data_path() + "/test.yaml")

    # Act
    da_layer = DataAccessLayer(logger)
    model_data = da_layer.read_input_file(path, logger)
    input_version = model_data.version

    # Assert
    # input_version should consist of 3 elements (major, minor, patch):
    assert len(input_version) == 3


def test_data_access_layer_provides_yaml_model_data_for_yaml_file():
    """The DataAccessLayer should provide a YamlModelData
    for a yaml file"""

    # Arrange
    logger = LoggerFactory.create_logger()
    path = Path(get_test_data_path() + "/test.yaml")

    # Act
    da_layer = DataAccessLayer(logger)
    model_data = da_layer.read_input_file(path)

    # Assert

    # implements interface
    assert isinstance(model_data, IModelData)
    assert isinstance(model_data, YamlModelData)

    assert model_data.name == "Model 1"
    assert len(model_data.datasets) == 1

    first_dataset = model_data.datasets[0]
    assert str(first_dataset.path).endswith("FM-VZM_0000_map.nc")
    assert "mesh2d_sa1" in first_dataset.mapping
    assert "mesh2d_s1" in first_dataset.mapping

    assert first_dataset.mapping["mesh2d_sa1"] == "mesh2d_sa1"
    assert first_dataset.mapping["mesh2d_s1"] == "water_level"


def test_data_access_layer_read_input_file_throws_exception_for_invalid_path():
    """The DataAccessLayer should throw a FileNotFoundError
    if the provided path for a yaml file does not exists"""

    # Arrange
    logger = Mock(ILogger)
    path = Path("test_invalid_path.yaml")
    da_layer = DataAccessLayer(logger)

    # Act
    with pytest.raises(FileExistsError) as exc_info:
        da_layer.read_input_file(path)

    exception_raised = exc_info.value

    # Assert
    assert isinstance(exception_raised, FileExistsError)
    expected_message = "ERROR: The input file test_invalid_path.yaml does not exist."
    assert exception_raised.args[0] == expected_message


def test_dataset_data_write_output_file_should_write_file():
    """When calling write_output_file on a dataset should
    write the specified XArray dataset to an output file
    """

    # Arrange
    logger = Mock(ILogger)
    path = Path(str(get_test_data_path()) + "/results.nc")
    da_layer = DataAccessLayer(logger)
    data = [1]
    time = pd.date_range("2020-01-01", periods=1)
    dataset = _xr.Dataset(data_vars=dict(data=(["time"], data)), coords=dict(time=time))

    # Act
    da_layer.write_output_file(dataset, path)

    # Assert
    assert path.is_file()


def test_dataset_data_write_output_file_should_check_if_path_exists():
    """When calling write_output_file the provided path
    needs to be checked if it exists"""

    # Arrange
    logger = Mock(ILogger)
    path = Path("./non_existing_dir/results.nc")
    da_layer = DataAccessLayer(logger)
    dataset = Mock(_xr.Dataset)

    # Act
    with pytest.raises(FileExistsError) as exc_info:
        da_layer.write_output_file(dataset, path)

    exception_raised = exc_info.value

    # Assert
    exc = exception_raised.args[0]
    assert exc.endswith("Make sure the output file location is valid.")


def test_dataset_data_write_output_file_should_check_if_extension_is_correct():
    """When calling write_output_file the provided path
    extension needs to be checked if it matches
    the currently implementation (netCDF files)"""

    # Arrange
    logger = Mock(ILogger)
    path = Path(str(get_test_data_path()) + "/NonUgridFile.txt")
    da_layer = DataAccessLayer(logger)
    dataset = Mock(_xr.Dataset)

    # Act
    with pytest.raises(NotImplementedError) as exc_info:
        da_layer.write_output_file(dataset, path)

    exception_raised = exc_info.value

    # Assert
    assert exception_raised.args[0].endswith(
        "Currently only UGrid (NetCDF) files are supported."
    )


def test_dataset_data_get_input_dataset_should_read_file():
    """When calling get_input_dataset on a dataset should
    read the specified IDatasetData.path to create a new DataSet
    """

    # Arrange
    logger = Mock(ILogger)
    path = get_test_data_path() + "/FlowFM_net.nc"
    data_dict = {
        "filename": path,
        "outputfilename": "output.txt",
        "variable_mapping": {"test": "test_new"},
    }
    data = DatasetData(data_dict)

    # Act
    da_layer = DataAccessLayer(logger)
    dataset = da_layer.read_input_dataset(data)

    # Assert
    assert isinstance(dataset, _xr.Dataset)


def test_dataset_data_get_input_dataset_should_check_if_path_exists():
    """When calling get_input_dataset the provided path
    needs to be checked if it exists"""

    # Arrange
    logger = Mock(ILogger)
    data_dict = {
        "filename": "non_existing_file.nc",
        "outputfilename": "output.txt",
        "variable_mapping": {"test": "test_new"},
    }
    data = DatasetData(data_dict)

    # Act
    da_layer = DataAccessLayer(logger)

    with pytest.raises(FileExistsError) as exc_info:
        da_layer.read_input_dataset(data)

    exception_raised = exc_info.value

    # Assert
    exc = exception_raised.args[0]
    assert exc.endswith("Make sure the input file location is valid.")


def test_dataset_data_get_input_dataset_should_check_if_extension_is_correct():
    """When calling get_input_dataset the provided path
    needs to be checked if it exists"""

    # Arrange
    logger = Mock(ILogger)
    path = get_test_data_path() + "/NonUgridFile.txt"
    data_dict = {
        "filename": path,
        "outputfilename": "output.txt",
        "variable_mapping": {"test": "test_new"},
    }
    data = DatasetData(data_dict)

    # Act
    da_layer = DataAccessLayer(logger)

    with pytest.raises(NotImplementedError) as exc_info:
        da_layer.read_input_dataset(data)

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
    logger = Mock(ILogger)
    path = get_test_data_path() + "/FlowFM_net_incorrect.nc"
    data_dict = {
        "filename": path,
        "outputfilename": "output.txt",
        "variable_mapping": {"test": "test_new"},
    }
    data = DatasetData(data_dict)

    # Act
    da_layer = DataAccessLayer(logger)

    with pytest.raises(ValueError) as exc_info:
        da_layer.read_input_dataset(data)

    exception_raised = exc_info.value
    # Assert

    path = Path(path).resolve()
    assert exception_raised.args[0].endswith(
        f"ERROR: Cannot open input .nc file -- {str(path)}"
    )


def test_data_access_layer_apply_time_filter():
    """The DataAccessLayer should apply a given time filter"""

    # Arrange
    logger = Mock(ILogger)
    path = get_test_data_path() + "/test_time_filter.nc"
    data_dict = {
        "filename": path,
        "start_date": "01-07-2014",
        "end_date": "31-08-2014",
        "variable_mapping": {"water_depth_m": "water_depth"}
    }
    input_data = DatasetData(data_dict)
    date_format = "%d-%m-%Y"
    start_date_expected = datetime.strptime("02-07-2014", date_format)
    end_date_expected = datetime.strptime("31-08-2014", date_format)

    # Act
    da_layer = DataAccessLayer(logger)
    ds_result = da_layer.read_input_dataset(input_data)
    ds_result_date = ds_result['time'].indexes['time'].normalize()
    min_date_result = ds_result_date.min()
    max_date_result = ds_result_date.max()

    # Assert
    # test if result is time filtered for both start and end date
    assert min_date_result == start_date_expected
    assert max_date_result == end_date_expected
