"""
Tests for DataAccessLayer class
"""

from unittest.mock import Mock

import pytest

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
    path = get_test_data_path() + "/test.yaml"

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
    assert first_dataset.path == "test/data/FM-VZM_0000_map.nc"
    assert "mesh2d_sa1" in first_dataset.mapping
    assert "mesh2d_s1" in first_dataset.mapping

    assert first_dataset.mapping["mesh2d_sa1"] == "mesh2d_sa1"
    assert first_dataset.mapping["mesh2d_s1"] == "water_level"


def test_data_access_layer_throws_exception_for_invalid_path():
    """The DataAccessLayer should throw a FileNotFoundError
    if the provided path for a yaml file does not exists"""

    # Arrange
    logger = Mock(ILogger)
    path = "test_invalid_path.yaml"
    da_layer = DataAccessLayer(logger)

    # Act
    with pytest.raises(FileExistsError) as exc_info:
        da_layer.read_input_file(path)

    exception_raised = exc_info.value

    # Assert

    assert isinstance(exception_raised, FileExistsError)
    expected_message = 'The input file test_invalid_path.yaml does not exist.'
    assert exception_raised.args[0] == expected_message
