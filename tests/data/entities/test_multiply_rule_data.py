"""
Tests for MultiplyRuleData class
"""

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.multiply_rule_data import MultiplyRuleData


def test_multiply_rule_data_creation_logic():
    """The MultiplyRuleData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = MultiplyRuleData("test_name", [1.0, 2.0], "input", "output")

    # Assert

    assert isinstance(data, IRuleData)
    assert data.input_variable == "input"
    assert data.multipliers == [1.0, 2.0]
