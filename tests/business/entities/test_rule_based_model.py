"""
Tests for RuleBasedModel class
"""


from unittest.mock import Mock

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


def test_status_setter():
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

    rule.input_variable_names = ["test"]
    rule.output_variable_name = "output"

    no_rules_and_datasets_model = RuleBasedModel([], [], logger)
    no_rules_model = RuleBasedModel([dataset], [], logger)
    no_datasets_model = RuleBasedModel([], [rule], logger)
    model = RuleBasedModel([dataset], [rule], logger)

    # Act & Assert

    assert not no_rules_and_datasets_model.validate(logger)
    assert not no_rules_model.validate(logger)
    assert not no_datasets_model.validate(logger)
    assert model.validate(logger)


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
