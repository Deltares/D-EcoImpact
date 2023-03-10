"""
Tests for RuleBasedModel class
"""


from unittest.mock import MagicMock, Mock

import pytest
import xarray as _xr

from decoimpact.business.entities.i_model import ModelStatus
from decoimpact.business.entities.rule_based_model import RuleBasedModel
from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.i_multi_array_based_rule import (
    IMultiArrayBasedRule,
)
from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_dataset import IDatasetData


def test_create_rule_based_model_with_defaults():
    """Test that the default properties of a rule-based model
    are set when creating the model using the default constructor."""

    # Arrange
    rule = Mock(IRule)
    dataset = Mock(IDatasetData)

    # Act
    model = RuleBasedModel([dataset], [rule])

    # Assert

    assert isinstance(model, RuleBasedModel)
    assert model.name == "Rule-Based model"
    assert rule in model.rules
    assert dataset in model.input_datasets
    assert model.status == ModelStatus.CREATED


def test_status_setter():
    """Test if status is correctly set for a model"""

    # Arrange
    rule = Mock(IRule)
    dataset = Mock(IDatasetData)
    logger = Mock(ILogger)

    # Act
    model = RuleBasedModel([dataset], [rule], logger)

    assert model.status == ModelStatus.CREATED
    model.status = ModelStatus.EXECUTED
    assert model.status == ModelStatus.EXECUTED


def test_validation_of_rule_based_model():
    """Test if the model correctly validates for required
    parameters (datasets, rules)
    """

    # Arrange
    rule = Mock(IRule)
    dataset = _xr.Dataset()
    logger = Mock(ILogger)

    dataset["test"] = _xr.DataArray([32, 94, 9])

    rule.input_variable_names = ["input"]
    rule.output_variable_name = "output"

    mapping_usual = {"test": "input"}
    model_usual = RuleBasedModel([dataset], [rule], mapping_usual)

    map_to_itself = {"test": "test"}
    model_map_to_itself = RuleBasedModel([dataset], [rule], map_to_itself)

    map_non_existing_var = {"non_existing_var": "input"}
    model_map_non_existing_var = RuleBasedModel([dataset], [rule], map_non_existing_var)

    map_to_wrong_var = {"test": "incorrect_var"}
    model_map_to_wrong_var = RuleBasedModel([dataset], [rule], map_to_wrong_var)

    map_from_non_existing_var_to_wrong_var = {"non_existing_var": "incorrect_var"}
    model_map_from_non_existing_var_to_wrong_var = RuleBasedModel(
        [dataset], [rule], map_from_non_existing_var_to_wrong_var
    )

    model_no_rules_and_datasets = RuleBasedModel([], [])
    model_no_rules = RuleBasedModel([dataset], [])
    model_no_datasets_model = RuleBasedModel([], [rule])

    # Act & Assert
    assert model_usual.validate(logger)
    assert not model_map_to_itself.validate(logger)
    assert not model_map_non_existing_var.validate(logger)
    assert not model_map_to_wrong_var.validate(logger)
    assert not model_map_from_non_existing_var_to_wrong_var.validate(logger)
    assert not model_no_rules_and_datasets.validate(logger)
    assert not model_no_rules.validate(logger)
    assert not model_no_datasets_model.validate(logger)


def test_error_initializing_rule_based_model():
    """Tests if the error message sent when initializing a rule based model fails."""
    # Arrange
    dataset = _xr.Dataset()
    dataset["test"] = _xr.DataArray([32, 94, 9])
    rule: IRule = Mock(IRule)
    rule.input_variable_names = ["unknown_var"]  # ["unknown_var"]
    rule.name = "rule with unknown var"
    model = RuleBasedModel([dataset], [rule])
    logger = Mock(ILogger)

    # Act
    model.initialize(logger)

    # Assert
    logger.log_error.assert_called_with("Initialization failed.")


def test_error_executing_model_with_processor_none():
    """
    Tests the error thrown when the processor of a rule based model is None.
    """
    # Arrange
    dataset = _xr.Dataset()
    dataset["test"] = _xr.DataArray([32, 94, 9])
    rule: IRule = Mock(IRule)
    logger = Mock(ILogger)
    model = RuleBasedModel([dataset], [rule])
    model._rule_processor = None

    # Act
    with pytest.raises(RuntimeError) as exc_info:
        model.execute(logger)
    exception_raised = exc_info.value

    # Assert
    expected_message = "Processor is not set, please initialize model."
    assert exception_raised.args[0] == expected_message


def test_validation_of_rule_based_model_rule_dependencies():
    """Test if the model correctly validates the given
    rules for dependencies"
    """
    # Arrange
    dataset = _xr.Dataset()
    dataset["test"] = _xr.DataArray([32, 94, 9])
    rule: IRule = Mock(IRule)
    logger = Mock(ILogger)

    rule.validate.return_value = True

    model = RuleBasedModel([dataset], [rule])

    # Act & Assert
    assert model.validate(logger)
    rule.validate.assert_called_once_with(logger)


def test_run_rule_based_model():
    """Test if the model can correctly run the given
    rules and adds the calculated results"

           +------+
    test --|  R1  |-- out1 --+
           +------+          |  +-----+
                             +--|     |
                                |  R3 |-- out3
                             +--|     |
           +------+          |  +-----+
    test --|  R2  |-- out2 --+
           +------+
    """
    # Arrange
    dataset = _xr.Dataset()
    dataset["test"] = _xr.DataArray([32, 94, 9])
    dataset["test"].attrs = {"cf_role": "mesh_topology"}

    logger = Mock(ILogger)
    rule1 = Mock(IArrayBasedRule, id="rule1")
    rule2 = Mock(IArrayBasedRule, id="rule2")
    rule3 = Mock(IMultiArrayBasedRule, id="rule3")

    rule1.input_variable_names = ["test"]
    rule2.input_variable_names = ["test"]
    rule3.input_variable_names = ["out1", "out2"]

    rule1.output_variable_name = "out1"
    rule2.output_variable_name = "out2"
    rule3.output_variable_name = "out3"

    rule1.execute.return_value = _xr.DataArray([32, 94, 9])
    rule2.execute.return_value = _xr.DataArray([32, 94, 9])
    rule3.execute.return_value = _xr.DataArray([32, 94, 9])

    model = RuleBasedModel([dataset], [rule1, rule2, rule3])

    # Act
    assert model.validate(logger)
    model.initialize(logger)
    model.execute(logger)
    model.finalize(logger)

    # Assert
    assert "out1" in model.output_dataset.keys()
    assert "out2" in model.output_dataset.keys()
    assert "out3" in model.output_dataset.keys()


def test_make_output_variables_list():
    # Arrange
    vars = ("var1", "var2", "var3", "var4", "var5")
    dataset = _xr.Dataset(data_vars=dict.fromkeys(vars))
    dataset["var1"].attrs = {"cf_role": "mesh_topology", "test_bounds": "var2"}
    dataset["var2"].attrs = {"test_connectivity": "var4"}
    dataset["var3"].attrs = {"test_connectivity": "var5"}
    dataset["var4"].attrs = {"test_dimension": "test"}

    model = RuleBasedModel([dataset], [])

    var_list = model._make_output_variables_list()
    assert sorted(var_list) == sorted(["var1", "var2", "var4"])
