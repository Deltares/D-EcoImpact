"""
Tests for YamlModelData class
"""


from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.entities.yaml_model_data import YamlModelData


def test_yaml_model_data_default_settings_and_type():
    """Test if the YamlModelData implements the IModelData
    interface and gives the right default settings"""

    # Arrange
    yaml_contents = {"input-data": [], "rules": []}

    # Act
    model_data = YamlModelData("Model 1", yaml_contents)

    # Assert

    # implements interface
    assert isinstance(model_data, IModelData)

    assert model_data.name == "Model 1"
