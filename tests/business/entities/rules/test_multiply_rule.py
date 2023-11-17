# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for RuleBase class
"""


from unittest.mock import Mock

import numpy as _np
import xarray as _xr

from decoimpact.business.entities.rules.multiply_rule import MultiplyRule
from decoimpact.crosscutting.i_logger import ILogger


def test_create_multiply_rule_should_set_defaults():
    """Test creating a multiply rule with defaults"""

    # Arrange & Act
    rule = MultiplyRule("test", ["foo"], [[0.5, 3.0]])
    # Assert
    assert rule.name == "test"
    assert rule.description == ""
    assert rule.input_variable_names == ["foo"]
    assert rule.output_variable_name == "output"
    assert rule.multipliers == [[0.5, 3.0]]
    assert rule.date_range == None
    assert isinstance(rule, MultiplyRule)


def test_execute_value_array_multiplied_by_multipliers_no_dates():
    """Test executing Multiply Rule with single multipliers and
    no date range."""

    # Arrange
    logger = Mock(ILogger)
    rule = MultiplyRule("test", ["foo"], [[0.5, 4.0]], description="description")
    data = [1, 2, 3, 4]
    value_array = _xr.DataArray(data)

    # Act
    multiplied_array = rule.execute(value_array, logger)

    result_data = [2.0, 4.0, 6.0, 8.0]
    result_array = _xr.DataArray(result_data)

    # Assert
    assert _xr.testing.assert_equal(multiplied_array, result_array) is None


def test_execute_value_array_multiplied_by_multipliers_with_dates():
    """Test executing Multiply Rule with multipliers and a date range."""

    # Arrange
    logger = Mock(ILogger)
    rule = MultiplyRule(
        "test",
        ["foo"],
        [[1], [100, 10]],
        date_range=[["01-01", "10-01"], ["11-01", "20-01"]]
    )

    values = [0.1, 0.7, 0.2, 0.2, 0.3, 0.1]
    time = [
        "2020-01-02",
        "2020-01-12",
        "2021-01-03",
        "2021-01-13",
        "2022-01-04",
        "2022-01-14",
    ]
    time = [_np.datetime64(t) for t in time]
    value_array = _xr.DataArray(values, coords=[time], dims=["time"])

    # Act
    multiplied_array = rule.execute(value_array, logger)

    result_data = [0.1, 700, 0.2, 200, 0.3, 100]
    result_array = _xr.DataArray(result_data, coords=[time], dims=["time"])

    # Assert
    assert _xr.testing.assert_equal(multiplied_array, result_array) is None


def test_execute_value_array_multiplied_by_multipliers_with_dates_missing_dates():
    """Test executing Multiply Rule with multipliers and a date range. And check 
    that the values that are outside the given periods are filled with None"""

    # Arrange
    logger = Mock(ILogger)
    rule = MultiplyRule(
        "test",
        ["foo"],
        [[2], [100, 10]],
        date_range=[["02-01", "10-01"], ["11-01", "20-01"]]
    )

    values = [0.1, 0.7, 0.2, 0.2, 0.3, 0.1]
    time = [
        "2020-01-02",
        "2020-01-12",
        "2021-01-03",
        "2021-01-13",
        "2022-01-04",
        "2022-01-14",
    ]
    time = [_np.datetime64(t) for t in time]
    value_array = _xr.DataArray(values, coords=[time], dims=["time"])

    # Act
    multiplied_array = rule.execute(value_array, logger)

    result_data = [None, 700, 0.4, 200, 0.6, 100]
    result_array = _xr.DataArray(result_data, coords=[time], dims=["time"])

    # Assert
    assert _xr.testing.assert_equal(multiplied_array, result_array) is None
