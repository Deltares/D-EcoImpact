"""
Tests for ModelFactory class
"""


from unittest.mock import Mock

import pytest

from decoimpact.business.entities.rule_based_model import RuleBasedModel
from decoimpact.business.entities.rules.combine_results_rule import CombineResultsRule
from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.business.entities.rules.operation_type import OperationType
from decoimpact.business.workflow.model_factory import ModelFactory
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.combine_results_rule_data import CombineResultsRuleData
from decoimpact.data.entities.multiply_rule_data import MultiplyRuleData


def test_create_rule_based_model():
    """Test creating a rule-based model via factory"""

    # Arrange
    logger = Mock(ILogger)
    model_data = Mock(IModelData)
    dataset = Mock()
    dataset_data = Mock(IDatasetData)

    rules_data = MultiplyRuleData("abc", [2, 5.86], "a", "b")

    model_data.name = "Test model"
    model_data.datasets = [dataset_data]
    model_data.rules = [rules_data]

    dataset_data.get_input_dataset.return_value = dataset

    # Act
    model = ModelFactory.create_model(logger, model_data)

    # Assert

    assert isinstance(model, RuleBasedModel)
    assert model.name == "Test model"
    assert dataset in model.input_datasets
    assert len(model.rules) == 1

    # logs info about model creation
    logger.log_info.assert_called_once()


def test_create_combine_results_rule_from_data_object():
    """Test creating a rule-based model via factory"""

    # Arrange
    rule_data = CombineResultsRuleData("abc", ["a", "b"], "Multiply", "c")

    # Act
    rule = ModelFactory._create_rule(rule_data)

    # Assert
    assert isinstance(rule, CombineResultsRule)
    assert rule.name == "abc"
    assert rule.input_variable_names == ["a", "b"]
    assert rule.operation_type == OperationType.MULTIPLY
    assert rule.output_variable_name == "c"


def test_create_rule_based_model_with_non_supported_rule():
    """Test creating a rule-based model with a rule that is
    not supported/recognized by the builder.
    This should throw an exception"""

    # Arrange
    logger = Mock(ILogger)
    model_data = Mock(IModelData)
    dataset_data = Mock(IDatasetData)

    rules_data = Mock(IRuleData)

    rules_data.name = "test"

    model_data.name = "Test model"
    model_data.datasets = [dataset_data]
    model_data.rules = [rules_data]

    dataset_data.get_input_dataset.return_value = []

    # Act & Assert
    with pytest.raises(NotImplementedError) as exc_info:
        ModelFactory.create_model(logger, model_data)

    exception_raised = exc_info.value

    # Assert
    expected_message = "The rule type of rule 'test' is currently " "not implemented"
    assert exception_raised.args[0] == expected_message
