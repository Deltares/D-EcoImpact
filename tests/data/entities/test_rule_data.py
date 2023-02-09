"""
Tests for RuleData class
"""

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.rule_data import RuleData


def test_rule_data_creation_logic():
    """The RuleData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Arrange
    data_dict = {"test_name": {"foo": "bar"}}

    # Act
    data = RuleData(data_dict)

    # Assert

    assert isinstance(data, IRuleData)
    assert data.name == "test_name"
    assert data.data == {"foo": "bar"}
