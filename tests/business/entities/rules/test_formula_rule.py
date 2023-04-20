"""
Tests for RuleBase class
"""


from unittest.mock import Mock

import xarray as _xr
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
    value_arrays = {
        "foo": _xr.DataArray([1, 2, 3, 4]),
        "bar": _xr.DataArray([4, 3, 2, 1]),
    }

    # Act
    formula_array = rule.execute_multiple_input(value_arrays, logger)

    result_data = [5, 5, 5, 5]
    result_array = _xr.DataArray(result_data)

    # Assert
    assert _xr.testing.assert_equal(formula_array, result_array) is None


def test_execute_multiplying_value_arrays():
    """Test formula on value_arrays of a RuleBase"""

    # Arrange
    logger = Mock(ILogger)
    rule = FormulaRule("test", ["foo", "bar"], "foo * bar", "outputname")
    value_arrays = {
        "foo": _xr.DataArray([1, 2, 3, 4]),
        "bar": _xr.DataArray([4, 3, 2, 1]),
    }

    # Act
    formula_array = rule.execute_multiple_input(value_arrays, logger)

    result_data = [4, 6, 6, 4]
    result_array = _xr.DataArray(result_data)

    # Assert
    assert _xr.testing.assert_equal(formula_array, result_array) is None


def test_execute_comparing_value_arrays():
    """Test formula on value_arrays of a RuleBase"""

    # Arrange
    logger = Mock(ILogger)
    rule = FormulaRule("test", ["foo", "bar"], "foo > bar", "outputname")
    value_arrays = {
        "foo": _xr.DataArray([1, 2, 3, 4]),
        "bar": _xr.DataArray([4, 3, 2, 1]),
    }

    # Act
    formula_array = rule.execute_multiple_input(value_arrays, logger)

    result_data = [0, 0, 1, 1]
    result_array = _xr.DataArray(result_data)

    # Assert
    assert _xr.testing.assert_equal(formula_array, result_array) is None


def test_execute_comparing_array_with_number():
    """Test formula on value_arrays of a RuleBase"""

    # Arrange
    logger = Mock(ILogger)
    rule = FormulaRule("test", ["foo"], "foo >= 1", "outputname")
    value_arrays = {"foo": _xr.DataArray([0, 1, 2, 3, 4])}

    # Act
    formula_array = rule.execute_multiple_input(value_arrays, logger)

    result_data = [0, 1, 1, 1, 1]
    result_array = _xr.DataArray(result_data)

    # Assert
    assert _xr.testing.assert_equal(formula_array, result_array) is None


def test_execute_if_else_on_array():
    """Test formula on value_arrays of a RuleBase"""

    # Arrange
    logger = Mock(ILogger)
    rule = FormulaRule("test", ["foo"], "foo >= 1", "outputname")
    value_arrays = {"foo": _xr.DataArray([0, 1, 2, 3, 4])}

    # Act
    formula_array = rule.execute_multiple_input(value_arrays, logger)

    result_data = [0, 1, 1, 1, 1]
    result_array = _xr.DataArray(result_data)

    # Assert
    assert _xr.testing.assert_equal(formula_array, result_array) is None


def test_execute_unwanted_python_code():
    """Test formula on value_arrays of a RuleBase"""

    # Arrange
    logger = Mock(ILogger)
    rule = FormulaRule("test", ["foo", "bar"], "print('hoi')", "outputname")
    value_arrays = {
        "foo": _xr.DataArray([1, 2, 3, 4]),
        "bar": _xr.DataArray([4, 3, 2, 1]),
    }

    # Act
    with pytest.raises(NameError) as exc_info:
        rule.execute_multiple_input(value_arrays, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "name '_print_' is not defined"
    assert exception_raised.args[0] == expected_message


def test_formula_has_incorrect_variable_names():
    """Test formula on value_arrays of a RuleBase"""

    # Arrange
    logger = Mock(ILogger)
    rule = FormulaRule("test", ["foo", "bar"], "foo + bas", "outputname")
    value_arrays = {
        "foo": _xr.DataArray([1, 2, 3, 4]),
        "bar": _xr.DataArray([4, 3, 2, 1]),
    }

    # Act
    with pytest.raises(NameError) as exc_info:
        rule.execute_multiple_input(value_arrays, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "name 'bas' is not defined"
    assert exception_raised.args[0] == expected_message


def test_incorrect_variable_names_in_values_dict():
    """Test formula on value_arrays of a RuleBase"""

    # Arrange
    logger = Mock(ILogger)
    rule = FormulaRule("test", ["foo", "bas"], "foo + bar", "outputname")
    value_arrays = {
        "foo": _xr.DataArray([1, 2, 3, 4]),
        "bas": _xr.DataArray([4, 3, 2, 1]),
    }

    # Act
    with pytest.raises(NameError) as exc_info:
        rule.execute_multiple_input(value_arrays, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "name 'bar' is not defined"
    assert exception_raised.args[0] == expected_message


# # nieuwe tests:
# 1. array > getal
# 2. tijdsarray van elkaar aftrekken (volkerak zoommeer)
# 3. if else statements
