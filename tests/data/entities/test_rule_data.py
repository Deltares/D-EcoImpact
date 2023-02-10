"""
Tests for RuleData class
"""

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.rule_data import RuleData


def test_rule_data_creation_logic():
    """The RuleData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = RuleData("test_name", output_variable="foo")

    # Assert

    assert isinstance(data, IRuleData)
    assert data.name == "test_name"
    assert data.description == ""
    assert data.output_variable == "foo"
