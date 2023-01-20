"""
Tests for RuleBasedModel class
"""


from decoimpact.business.entities.rule_based_model import RuleBasedModel


def test_create_rule_based_model_with_defaults():
    """Test that the default properties of a rule-based model
    is set when creating the model using the default constructor"""

    # Arrange & Act
    model = RuleBasedModel()

    # Assert

    assert isinstance(model, RuleBasedModel)
    assert model.name == "Rule-Based model"
    assert model.rules == []
