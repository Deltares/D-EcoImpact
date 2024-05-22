# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
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
from decoimpact.data.api.time_operation_type import TimeOperationType
from decoimpact.data.entities.combine_results_rule_data import CombineResultsRuleData
from decoimpact.data.entities.formula_rule_data import FormulaRuleData
from decoimpact.data.entities.layer_filter_rule_data import LayerFilterRuleData
from decoimpact.data.entities.multiply_rule_data import MultiplyRuleData
from decoimpact.data.entities.step_function_data import StepFunctionRuleData
from decoimpact.data.entities.time_aggregation_rule_data import TimeAggregationRuleData


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

    multiply_rule_data = MultiplyRuleData("abc", [2, 5.86], "a")
    multiply_rule_data.output_variable = "b"

    step_function_rule_data = StepFunctionRuleData(
        "step_function_name", [0.0, 20.0, 100.0], [1.0, 2.0, 3.0], "input_name"
    )
    step_function_rule_data.description = "descript_step_func_rule"
    step_function_rule_data.output_variable = "output_step_func_name"

    rule_data_layer_filter_rule = LayerFilterRuleData("lfrname", 2, "var1")
    rule_data_layer_filter_rule.output_variable = "output_name"

    time_aggregation_rule = TimeAggregationRuleData(
        "taname", TimeOperationType.MIN, 0, "var1", "Month"
    )
    time_aggregation_rule.output_variable = "output"

    combine_results_rule_data = CombineResultsRuleData(
        "test_rule_name", ["foo", "hello"], "MULTIPLY"
    )
    combine_results_rule_data.output_variable = "output"

    formula_rule_data = FormulaRuleData("test_rule_name", ["foo", "bar"], "foo + bar")
    formula_rule_data.output_variable = "output"

    model_data.name = "Test model"
    model_data.datasets = [dataset_data]
    model_data.rules = [
        multiply_rule_data,
        step_function_rule_data,
        combine_results_rule_data,
        rule_data_layer_filter_rule,
        time_aggregation_rule,
        formula_rule_data,
    ]

    da_layer.read_input_dataset.return_value = dataset
    model_builder = ModelBuilder(da_layer, logger)

    # Act
    model = model_builder.build_model(model_data)

    # Assert

    assert isinstance(model, RuleBasedModel)
    assert model.name == "Test model"
    assert dataset in model.input_datasets
    assert len(model.rules) == 6

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
