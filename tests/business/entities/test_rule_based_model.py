"""
Tests for RuleBasedModel class
"""


from unittest.mock import Mock
from decoimpact.business.entities.rule_based_model import RuleBasedModel


def test_create_rule_based_model_with_defaults():
    """Test that the default properties of a rule-based model
    is set when creating the model using the default constructor"""

    # Arrange
    rule = Mock()
    dataset = Mock()

    # Act
    model = RuleBasedModel([dataset], [rule])

    # Assert

    assert isinstance(model, RuleBasedModel)
    assert model.name == "Rule-Based model"
    assert rule in model.rules
    assert dataset in model.input_datasets
