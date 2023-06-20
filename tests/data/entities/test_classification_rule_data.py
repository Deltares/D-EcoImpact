"""
Tests for ClassificationRuleData class
"""

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.classification_rule_data import ClassificationRuleData


def test_classification_rule_data_creation_logic():
    """The ClassificationRuleData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Arrange
    test_table = [
        ["a", "output"],
        [1, 2]
    ]

    # Act
    data = ClassificationRuleData("test_name", ["foo", "bar"], test_table, "output", "description")

    # Assert

    assert isinstance(data, IRuleData)
    assert data.criteria_table == test_table
    assert data.input_variable_names == ["foo", "bar"]
