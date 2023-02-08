"""
Tests for RuleBasedModel class
"""


from unittest.mock import Mock

from decoimpact.business.entities.i_model import ModelStatus
from decoimpact.business.entities.rule_based_model import RuleBasedModel
from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_dataset import IDatasetData


def test_create_rule_based_model_with_defaults():
    """Test that the default properties of a rule-based model
    is set when creating the model using the default constructor"""

    # Arrange
    rule = Mock(IRule)
    logger = Mock(ILogger)
    dataset = Mock(IDatasetData)

    # Act
    model = RuleBasedModel([dataset], [rule], logger)

    # Assert

    assert isinstance(model, RuleBasedModel)
    assert model.name == "Rule-Based model"
    assert rule in model.rules
    assert dataset in model.input_datasets
    assert model.status == ModelStatus.CREATED


def test_validation_of_rule_based_model():
    """Test if the model correctly validates for required
    parameters (datasets, rules)
    """

    # Arrange
    rule = Mock(IRule)
    logger = Mock(ILogger)
    dataset = Mock(IDatasetData)

    no_rules_and_datasets_model = RuleBasedModel([], [], logger)
    no_rules_model = RuleBasedModel([dataset], [], logger)
    no_datasets_model = RuleBasedModel([], [rule], logger)
    model = RuleBasedModel([dataset], [rule], logger)

    # Act & Assert

    assert not no_rules_and_datasets_model.validate()
    assert not no_rules_model.validate()
    assert not no_datasets_model.validate()
    assert model.validate()
