"""
Tests for DataAccessLayer class
"""

from pathlib import Path
from unittest.mock import Mock

import pandas as pd
import pytest
import xarray as _xr

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.crosscutting.logger_factory import LoggerFactory
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.entities.data_access_layer import DataAccessLayer
from decoimpact.data.entities.yaml_model_data import YamlModelData
from tests.testing_utils import get_test_data_path


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
    assert first_dataset.inputpath.endswith("FM-VZM_0000_map.nc")
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
    assert exc.endswith("Make sure the outputfile location is valid.")


def test_dataset_data_write_output_file_should_check_if_extension_is_correct():
    """When calling write_output_file the provided path
    extension needs to be checked if it matches the currently implementation (netCDF files)"""

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
