"""
Tests for ModelFactory class
"""


from unittest.mock import Mock

import pytest

from decoimpact.business.entities.rule_based_model import RuleBasedModel
from decoimpact.business.workflow.model_builder import ModelBuilder
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_data_access_layer import IDataAccessLayer
from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.multiply_rule_data import MultiplyRuleData
from decoimpact.data.entities.step_function_data import StepFunctionRuleData


def test_create_multiply_rule_based_model():
    """Test creating a multiply-rule-based model via factory"""


def test_create_rule_based_model():
    """Test creating a rule-based model via builder"""

    # Arrange
    logger = Mock(ILogger)
    model_data = Mock(IModelData)
    dataset = Mock()
    dataset_data = Mock(IDatasetData)
    da_layer = Mock(IDataAccessLayer)

    rules_data = MultiplyRuleData("abc", [2, 5.86], "a", "b")
    rule_data_step_function = StepFunctionRuleData(
        "step_function_name",
        [0.0, 20.0, 100.0],
        [1.0, 2.0, 3.0],
        "input_name",
        "descript_step_func_rule",
        "output_step_func_name",
    )

    model_data.name = "Test model"
    model_data.datasets = [dataset_data]
    model_data.rules = [rules_data, rule_data_step_function]

    da_layer.read_input_dataset.return_value = dataset
    model_builder = ModelBuilder(da_layer, logger)

    # Act
    model = model_builder.build_model(model_data)

    # Assert

    assert isinstance(model, RuleBasedModel)
    assert model.name == "Test model"
    assert dataset in model.input_datasets
    assert len(model.rules) == 2

    # logs info about model creation
    logger.log_info.assert_called_once()


def test_create_rule_based_model_with_non_supported_rule():
    """Test creating a rule-based model with a rule that is
    not supported/recognized by the builder.
    This should throw an exception"""

    # Arrange
    logger = Mock(ILogger)
    model_data = Mock(IModelData)
    dataset_data = Mock(IDatasetData)
    da_layer = Mock(IDataAccessLayer)

    rules_data = Mock(IRuleData)

    rules_data.name = "test"

    model_data.name = "Test model"
    model_data.datasets = [dataset_data]
    model_data.rules = [rules_data]

    model_builder = ModelBuilder(da_layer, logger)

    # Act & Assert
    with pytest.raises(NotImplementedError) as exc_info:
        model_builder.build_model(model_data)

    exception_raised = exc_info.value

    # Assert
    expected_message = "The rule type of rule 'test' is currently not implemented"
    assert exception_raised.args[0] == expected_message
