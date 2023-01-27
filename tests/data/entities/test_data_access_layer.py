"""
Tests for DataAccessLayer class
"""


from decoimpact.crosscutting.logger_factory import LoggerFactory
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.entities.data_access_layer import DataAccessLayer
from decoimpact.data.entities.yaml_model_data import YamlModelData


def test_data_access_layer_provides_yaml_model_data_for_yaml_file():
    """The DataAccessLayer should provide a YamlModelData
    for a yaml file"""

    # Arrange & Act
    logger = LoggerFactory.create_logger()

    # Assert
    da_layer = DataAccessLayer(logger)
    model_data = da_layer.read_input_file("test.yaml")

    # implements interface
    assert isinstance(model_data, IModelData)
    assert isinstance(model_data, YamlModelData)

    assert model_data.name == "Model 1"
