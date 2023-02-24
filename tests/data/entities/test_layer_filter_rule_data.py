"""
Tests for LayerFilterRuleData class
"""

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.layer_filter_rule_data import LayerFilterRuleData


def test_layer_filter_rule_data_creation_logic():
    """The LayerFilterRuleData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = LayerFilterRuleData("test_name", 3, "input", "output", "description")

    # Assert

    assert isinstance(data, IRuleData)
    assert data.input_variable == "input"
    assert data.layer_number == 3
