# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the 
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for RuleBase class
"""


from unittest.mock import Mock

import pytest

from decoimpact.business.entities.rules.formula_rule import FormulaRule
from decoimpact.crosscutting.i_logger import ILogger


def test_create_formula_rule_should_set_defaults():
    """Test creating a RuleBase with defaults"""

    # Arrange & Act
    rule = FormulaRule("test", ["foo", "bar"], "foo + bar", "outputname")
    # Assert
    assert rule.name == "test"
    assert rule.description == ""
    assert rule.input_variable_names == ["foo", "bar"]
    assert rule.output_variable_name == "outputname"
    assert rule.formula == "foo + bar"
    assert isinstance(rule, FormulaRule)


def test_execute_adding_value_arrays():
    """Test formula on value_arrays of a RuleBase"""

    # Arrange
    logger = Mock(ILogger)
    rule = FormulaRule("test", ["foo", "bar"], "foo + bar", "outputname")
    values = {"foo": 1.0, "bar": 4.0}

    # Act
    result_value = rule.execute(values, logger)

    # Assert
    assert result_value == 5.0


def test_execute_multiplying_value_arrays():
    """Test formula on value_arrays of a RuleBase"""

    # Arrange
    logger = Mock(ILogger)
    rule = FormulaRule("test", ["foo", "bar"], "foo * bar", "outputname")
    values = {
        "foo": 2.0,
        "bar": 3.0,
    }

    # Act
    result_value = rule.execute(values, logger)

    # Assert
    assert result_value == 6.0


@pytest.mark.parametrize(
    "input_value1, input_value2, expected_output_value",
    [(0.5, 10, 0.0), (11, 1.5, 1.0)],
)
def test_execute_comparing_value_arrays(
    input_value1: float, input_value2: float, expected_output_value: float
):
    """Test formula on value_arrays of a RuleBase"""

    # Arrange
    logger = Mock(ILogger)
    rule = FormulaRule("test", ["foo", "bar"], "foo > bar", "outputname")
    values = {
        "foo": input_value1,
        "bar": input_value2,
    }

    # Act
    result_value = rule.execute(values, logger)

    # Assert
    assert result_value == expected_output_value


def test_execute_unwanted_python_code():
    """Test formula on value_arrays of a RuleBase"""

    # Arrange
    logger = Mock(ILogger)
    rule = FormulaRule("test", ["foo", "bar"], "print('hoi')", "outputname")
    values = {
        "foo": 2.0,
        "bar": 3.0,
    }

    # Act
    with pytest.raises(NameError) as exc_info:
        rule.execute(values, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "name '_print_' is not defined"
    assert exception_raised.args[0] == expected_message


def test_formula_has_incorrect_variable_names():
    """Test formula on value_arrays of a RuleBase"""

    # Arrange
    logger = Mock(ILogger)
    rule = FormulaRule("test", ["foo", "bar"], "foo + bas", "outputname")
    values = {
        "foo": 2.0,
        "bar": 3.0,
    }

    # Act
    with pytest.raises(NameError) as exc_info:
        rule.execute(values, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "name 'bas' is not defined"
    assert exception_raised.args[0] == expected_message


@pytest.mark.parametrize(
    "formula, expected_output_value",
    [("print('hoi')", False), ("foo + bar", True), ("output=foo + bar", True)],
)
def test_validate_of_invalid_python_code(formula: str, expected_output_value: bool):
    """Test formula on value_arrays of a RuleBase"""

    # Arrange
    logger = Mock(ILogger)
    rule = FormulaRule("test", ["foo", "bar"], formula, "outputname")

    # Act
    result = rule.validate(logger)

    # Assert
    assert result == expected_output_value
