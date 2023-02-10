"""
Tests for RuleBasedModel class
"""


from unittest.mock import MagicMock, Mock, PropertyMock

import xarray as _xr

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
    dataset = Mock(IDatasetData)

    # Act
    model = RuleBasedModel([dataset], [rule])

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
    dataset = _xr.Dataset()
    logger = Mock(ILogger)

    dataset["test"] = _xr.DataArray([32, 94, 9])

    type(rule).input_variable_names = ["test"]
    type(rule).output_variable_name = "output"

    no_rules_and_datasets_model = RuleBasedModel([], [])
    no_rules_model = RuleBasedModel([dataset], [])
    no_datasets_model = RuleBasedModel([], [rule])
    model = RuleBasedModel([dataset], [rule])

    # Act & Assert

    assert not no_rules_and_datasets_model.validate(logger)
    assert not no_rules_model.validate(logger)
    assert not no_datasets_model.validate(logger)
    assert model.validate(logger)


def test_validation_of_rule_based_model_rule_dependencies():
    """Test if the model correctly validates the given
    rules for dependencies

           +------+
    test --|  R1  |-- out1 --+
           +------+          |  +-----+
                             +--|     |
                                |  R3 |-- out3 --+
                             +--|     |          |
           +------+          |  +-----+          |
    test --|  R2  |-- out2 --+                   |
           +------+                              |  +-----+
                                                 +--|     |
                                                    |  R4 |-- out4
    test -------------------------------------------|     |
                                                    +-----+
    """
    # Arrange
    dataset = _xr.Dataset()
    dataset["test"] = _xr.DataArray([32, 94, 9])

    logger = Mock(ILogger)

    rule1 = Mock(IRule, id="rule1")
    rule2 = Mock(IRule, id="rule2")
    rule3 = Mock(IRule, id="rule3")
    rule4 = Mock(IRule, id="rule4")

    type(rule1).input_variable_names = ["test"]
    type(rule2).input_variable_names = ["test"]
    type(rule3).input_variable_names = ["out1", "out2"]
    type(rule4).input_variable_names = ["out3", "test"]

    type(rule1).output_variable_name = "out1"
    type(rule2).output_variable_name = "out2"
    type(rule3).output_variable_name = "out3"
    type(rule4).output_variable_name = "out4"

    model = RuleBasedModel([dataset], [rule1, rule2, rule3, rule4])

    # Act & Assert
    assert model.validate(logger)

