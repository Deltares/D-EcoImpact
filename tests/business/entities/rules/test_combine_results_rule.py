# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the 
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for RuleBase class
"""

from typing import List
from unittest.mock import Mock

import numpy as _np
import pytest
import xarray as _xr

from decoimpact.business.entities.rules.combine_results_rule import CombineResultsRule
from decoimpact.business.entities.rules.multi_array_operation_type import (
    MultiArrayOperationType,
)
from decoimpact.crosscutting.i_logger import ILogger


def test_create_combine_results_rule_with_defaults():
    """Test creating a combine results rule with defaults"""

    # Arrange & Act
    rule = CombineResultsRule(
        "test_rule_name", ["foo", "hello"], MultiArrayOperationType.MULTIPLY, "output"
    )
    # Assert
    assert isinstance(rule, CombineResultsRule)
    assert rule.name == "test_rule_name"
    assert rule.description == ""
    assert rule.input_variable_names == ["foo", "hello"]
    assert rule.operation_type == MultiArrayOperationType.MULTIPLY
    assert rule.output_variable_name == "output"


def test_no_validate_error_with_correct_rule():
    """Test a correct combine results rule validates without error"""

    # Arrange
    logger = Mock(ILogger)
    rule = CombineResultsRule(
        "test_rule_name", ["foo", "hello"], MultiArrayOperationType.MULTIPLY, "output"
    )

    # Act
    valid = rule.validate(logger)

    # Assert
    assert isinstance(rule, CombineResultsRule)
    assert valid


def test_create_combine_results_rule_with_all_fields():
    """Test creating a combine results rule with all fields"""

    # Arrange & Act
    rule = CombineResultsRule(
        "test_rule_name",
        ["foo", "hello"],
        MultiArrayOperationType.MULTIPLY,
        "output",
        "test description",
    )
    # Assert
    assert isinstance(rule, CombineResultsRule)
    assert rule.name == "test_rule_name"
    assert rule.description == "test description"
    assert rule.input_variable_names == ["foo", "hello"]
    assert rule.operation_type == MultiArrayOperationType.MULTIPLY
    assert rule.output_variable_name == "output"


def test_execute_error_combine_results_rule_different_lengths():
    """Test setting input_variable_names of a RuleBase"""

    # Arrange & Act
    rule = CombineResultsRule(
        "test", ["foo_data", "hello_data"], MultiArrayOperationType.MULTIPLY, "output"
    )
    value_array = {"foo_data": _xr.DataArray([1, 2, 3]),
                   "hello_data": _xr.DataArray([4, 3, 2, 1])}

    # Assert
    with pytest.raises(ValueError) as exc_info:
        rule.execute(value_array, logger=Mock(ILogger))

    exception_raised = exc_info.value
    assert exception_raised.args[0] == "The arrays must have the same dimensions."


def test_execute_error_combine_results_rule_different_shapes():
    """Test setting input_variable_names of a RuleBase"""

    # Arrange & Act
    rule = CombineResultsRule(
        "test", ["foo_data", "hello_data"], MultiArrayOperationType.MULTIPLY, "output"
    )
    value_array = {"foo_data": _xr.DataArray([[1, 2], [3, 4]]),
                   "hello_data": _xr.DataArray([4, 3, 2, 1])}

    # Assert
    with pytest.raises(ValueError) as exc_info:
        rule.execute(value_array, logger=Mock(ILogger))

    exception_raised = exc_info.value
    assert exception_raised.args[0] == "The arrays must have the same dimensions."


@pytest.mark.parametrize(
    "operation, expected_result",
    [
        (MultiArrayOperationType.MIN, [4, 5, 3]),
        (MultiArrayOperationType.MAX, [20, 12, 24]),
        (MultiArrayOperationType.MULTIPLY, [1200, 420, 432]),
        (MultiArrayOperationType.AVERAGE, [13, 8, 11]),
        (MultiArrayOperationType.MEDIAN, [15, 7, 6]),
        (MultiArrayOperationType.ADD, [39, 24, 33]),
        (MultiArrayOperationType.SUBTRACT, [1, -10, -27]),
    ],
)
def test_all_operations_combine_results_rule(
    operation: MultiArrayOperationType, expected_result: List[float]
):
    """Test the outcome of each operand for the combine results rule"""
    # Arrange
    logger = Mock(ILogger)
    dict_vars = {"var1_name": _xr.DataArray([20, 7, 3]), 
                 "var2_name": _xr.DataArray([4, 5, 6]), 
                 "var3_name": _xr.DataArray([15, 12, 24])}
    # raw_data = [[20, 7, 3], [4, 5, 6], [15, 12, 24]]
    # xarray_data = [_xr.DataArray(arr) for arr in raw_data]

    # Act
    rule = CombineResultsRule(
        "test_name",
        ["var1_name", "var2_name", "var3_name"],
        operation,
        "output",
    )
    obtained_result = rule.execute(dict_vars, logger)

    # Assert
    _xr.testing.assert_equal(obtained_result, _xr.DataArray(expected_result))


def test_dims_present_in_result():
    """Test that the dims metadata of the result is equal to the one of the first xarray used."""
    # Arrange
    logger = Mock(ILogger)
    raw_data_1 = _np.ones((10, 20))
    raw_data_2 = 2 * _np.ones((10, 20))
    raw_data = [raw_data_1, raw_data_2]
    xarray_data = [
        _xr.DataArray(data=arr, dims=["test_dimension_1", "test_dimension_2"])
        for arr in raw_data
    ]
    dict_data = {"var1_name": xarray_data[0], "var2_name": xarray_data[1]}

    # Act
    rule = CombineResultsRule(
        "test_name",
        ["var1_name", "var2_name"],
        MultiArrayOperationType.ADD,
        "output",
    )
    obtained_result = rule.execute(dict_data, logger)

    # Assert
    # _xr.testing.assert_equal(obtained_result.dims, xarray_data[0].dims)
    assert obtained_result.dims == xarray_data[0].dims
