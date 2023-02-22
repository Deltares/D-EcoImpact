"""
Tests for RuleBase class
"""

from unittest.mock import Mock

import pytest
import xarray as _xr

from decoimpact.business.entities.rules.combine_results_rule import CombineResultsRule
from decoimpact.business.entities.rules.multi_array_operation_type import (
    MultiArrayOperationType,
)
from decoimpact.crosscutting.i_logger import ILogger


def test_create_combine_results_rule_should_set_defaults():
    """Test creating a RuleBase with defaults"""

    # Arrange & Act
    rule = CombineResultsRule(
        "test", ["foo", "hello"], MultiArrayOperationType.MULTIPLY, "output"
    )
    # Assert
    assert rule.name == "test"
    assert rule.description == ""
    assert rule.input_variable_names == ["foo", "hello"]
    assert rule.operation_type == MultiArrayOperationType.MULTIPLY
    assert rule.output_variable_name == "output"
    assert isinstance(rule, CombineResultsRule)


def test_execute_value_array_combine_results_rule_check_ndim():
    """Test setting input_variable_names of a RuleBase"""

    # Arrange & Act
    logger = Mock(ILogger)
    rule = CombineResultsRule(
        "test", ["foo_data", "hello_data"], MultiArrayOperationType.MULTIPLY, "output"
    )
    foo_data = [1, 2, 3]
    hello_data = [4, 3, 2, 1]
    value_array1 = _xr.DataArray(foo_data)
    value_array2 = _xr.DataArray(hello_data)

    # Act
    with pytest.raises(ValueError) as exc_info:
        rule.execute([value_array1, value_array2], logger)

    exception_raised = exc_info.value

    # Assert
    assert exception_raised.args[0] == "The arrays are not in the same dimension/shape!"


def test_execute_value_array_combine_results_rule_check_shape():
    """Test setting input_variable_names of a RuleBase"""

    # Arrange & Act
    logger = Mock(ILogger)
    rule = CombineResultsRule(
        "test", ["foo_data", "hello_data"], MultiArrayOperationType.MULTIPLY, "output"
    )
    foo_data = [[1, 2], [3, 4]]
    hello_data = [4, 3, 2, 1]
    value_array1 = _xr.DataArray(foo_data)
    value_array2 = _xr.DataArray(hello_data)

    # Act
    with pytest.raises(ValueError) as exc_info:
        rule.execute([value_array1, value_array2], logger)

    exception_raised = exc_info.value

    # Assert
    assert exception_raised.args[0] == "The arrays are not in the same dimension/shape!"


def test_execute_value_array_combine_results_rule_multiply():
    """Test setting input_variable_names of a RuleBase"""

    # Arrange & Act
    logger = Mock(ILogger)
    rule = CombineResultsRule(
        "test", ["foo_data", "hello_data"], MultiArrayOperationType.MULTIPLY, "output"
    )
    foo_data = [1, 2, 3, 4]
    hello_data = [4, 3, 2, 1]
    value_array1 = _xr.DataArray(foo_data)
    value_array2 = _xr.DataArray(hello_data)

    multiplied_array = rule.execute([value_array1, value_array2], logger)

    result_data = [4.0, 6.0, 6.0, 4.0]
    result_array = _xr.DataArray(result_data)

    # Assert
    _xr.testing.assert_equal(multiplied_array, result_array)


def test_execute_value_array_combine_results_rule_min():
    """Test setting input_variable_names of a RuleBase"""

    # Arrange & Act
    logger = Mock(ILogger)
    rule = CombineResultsRule(
        "test", ["foo_data", "hello_data"], MultiArrayOperationType.MIN, "output"
    )
    foo_data = [1, 2, 3, 4]
    hello_data = [4, 3, 2, 1]
    value_array1 = _xr.DataArray(foo_data)
    value_array2 = _xr.DataArray(hello_data)

    min_array = rule.execute([value_array1, value_array2], logger)

    result_data = [1.0, 2.0, 2.0, 1.0]
    result_array = _xr.DataArray(result_data)

    # Assert
    _xr.testing.assert_equal(min_array, result_array)


def test_execute_value_array_combine_results_rule_max():
    """Test setting input_variable_names of a RuleBase"""

    # Arrange & Act
    logger = Mock(ILogger)
    rule = CombineResultsRule(
        "test", ["foo_data", "hello_data"], MultiArrayOperationType.MAX, "output"
    )
    foo_data = [1, 2, 3, 4]
    hello_data = [4, 3, 2, 1]
    value_array1 = _xr.DataArray(foo_data)
    value_array2 = _xr.DataArray(hello_data)

    max_array = rule.execute([value_array1, value_array2], logger)

    result_data = [4.0, 3.0, 3.0, 4.0]
    result_array = _xr.DataArray(result_data)

    # Assert
    _xr.testing.assert_equal(max_array, result_array)


def test_execute_value_array_combine_results_rule_average():
    """Test setting input_variable_names of a RuleBase"""

    # Arrange & Act
    logger = Mock(ILogger)
    rule = CombineResultsRule(
        "test", ["foo_data", "hello_data"], MultiArrayOperationType.AVERAGE, "output"
    )
    foo_data = [1, 2, 3, 4]
    hello_data = [5, 3, 2, 1]
    value_array1 = _xr.DataArray(foo_data)
    value_array2 = _xr.DataArray(hello_data)

    ave_array = rule.execute([value_array1, value_array2], logger)

    result_data = [3, 2.5, 2.5, 2.5]
    result_array = _xr.DataArray(result_data)

    # Assert
    _xr.testing.assert_equal(ave_array, result_array)


def test_execute_value_array_combine_results_rule_median():
    """Test setting input_variable_names of a RuleBase"""

    # Arrange & Act
    logger = Mock(ILogger)
    rule = CombineResultsRule(
        "test", ["foo_data", "hello_data"], MultiArrayOperationType.MEDIAN, "output"
    )
    foo_data = [1, 2, 3, 4]
    hello_data = [5, 3, 2, 1]
    value_array1 = _xr.DataArray(foo_data)
    value_array2 = _xr.DataArray(hello_data)

    medi_array = rule.execute([value_array1, value_array2], logger)

    result_data = [3, 2.5, 2.5, 2.5]
    result_array = _xr.DataArray(result_data)

    # Assert
    _xr.testing.assert_equal(medi_array, result_array)


def test_execute_value_array_combine_results_rule_add():
    """Test setting input_variable_names of a RuleBase"""

    # Arrange & Act
    logger = Mock(ILogger)
    rule = CombineResultsRule(
        "test", ["foo_data", "hello_data"], MultiArrayOperationType.ADD, "output"
    )
    foo_data = [1, 2, 3, 4]
    hello_data = [5, 3, 2, 1]
    value_array1 = _xr.DataArray(foo_data)
    value_array2 = _xr.DataArray(hello_data)

    add_array = rule.execute([value_array1, value_array2], logger)

    result_data = [6, 5, 5, 5]
    result_array = _xr.DataArray(result_data)

    # Assert
    _xr.testing.assert_equal(add_array, result_array)


def test_execute_value_array_combine_results_rule_subtract():
    """Test setting input_variable_names of a RuleBase"""

    # Arrange & Act
    logger = Mock(ILogger)
    rule = CombineResultsRule(
        "test", ["foo_data", "hello_data"], MultiArrayOperationType.SUBTRACT, "output"
    )
    foo_data = [1, 2, 3, 4]
    hello_data = [5, 3, 2, 1]
    value_array1 = _xr.DataArray(foo_data)
    value_array2 = _xr.DataArray(hello_data)

    subs_array = rule.execute([value_array1, value_array2], logger)

    result_data = [-4, -1, 1, 3]
    result_array = _xr.DataArray(result_data)

    # Assert
    _xr.testing.assert_equal(subs_array, result_array)
