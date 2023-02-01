"""
Tests for DataAccessLayer class
"""


from decoimpact.crosscutting.logger_factory import LoggerFactory
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.entities.data_access_layer import DataAccessLayer
from decoimpact.data.entities.yaml_model_data import YamlModelData
from tests.testing_utils import get_test_data_path


def test_data_access_layer_provides_yaml_model_data_for_yaml_file():
    """The DataAccessLayer should provide a YamlModelData
    for a yaml file"""

    # Arrange & Act
    logger = LoggerFactory.create_logger()

    path = get_test_data_path() + "/test.yaml"

    # Assert
    da_layer = DataAccessLayer(logger)
    model_data = da_layer.read_input_file(path)

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
