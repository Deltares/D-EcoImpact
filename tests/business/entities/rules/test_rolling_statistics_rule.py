# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for rolling statistics rule
"""
import numpy as np
import pytest
import xarray as _xr
from mock import Mock

from decoimpact.business.entities.rules.rolling_statistics_rule import (
    RollingStatisticsRule,
)
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.time_operation_type import TimeOperationType

data = [0.1, 0.7, 0.2, 0.2, 0.3, 0.1]
time = [
    "2020-01-01",
    "2020-01-02",
    "2020-01-03",
    "2020-01-04",
    "2020-01-05",
    "2020-01-06",
]
time = [np.datetime64(t) for t in time]
value_array = _xr.DataArray(data, coords=[time], dims=["time"])


def test_create_rolling_statistics_rule_should_set_defaults():
    """Test creating a rolling statistics rule with defaults"""

    # Arrange & Act
    rule = RollingStatisticsRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.MIN,
    )

    # Assert
    assert rule.name == "test"
    assert rule.description == ""
    assert isinstance(rule, RollingStatisticsRule)


def test_rolling_statistics_rule_without_time_dimension():
    """RollingStatisticsRule should give an error when no time dim is defined"""
    # create test set
    logger = Mock(ILogger)
    rule = RollingStatisticsRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.ADD,
        time_scale="day",
        period=365,
    )

    test_data = [1.2, 0.4]
    test_array = _xr.DataArray(test_data, name="test_with_error")

    with pytest.raises(ValueError) as exc_info:
        rule.execute(test_array, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "No time dimension found for test_with_error"
    assert exception_raised.args[0] == expected_message


def test_execute_value_array_rolling_statistics_max():
    """RollingStatisticsRule (max, yearly)"""

    # create test set
    logger = Mock(ILogger)
    rule = RollingStatisticsRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.MAX,
        time_scale="day",
        period=2,
    )

    rolling_statistic = rule.execute(value_array, logger)

    result_data = [np.nan, np.nan, 0.7, 0.7, 0.3, 0.3]
    result_array = _xr.DataArray(result_data, coords=[time], dims=["time"])

    # Assert
    assert _xr.testing.assert_equal(rolling_statistic, result_array) is None
    
    
def test_execute_value_array_rolling_statistics_min():
    """RullingStatisticsRule (min, yearly)"""

    # create test set
    logger = Mock(ILogger)
    rule = RollingStatisticsRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.MIN,
        time_scale="day",
        period=2,
    )

    rolling_statistic = rule.execute(value_array, logger)

    result_data = [np.nan, np.nan, 0.1, 0.2, 0.2, 0.1]
    result_array = _xr.DataArray(result_data, coords=[time], dims=["time"])

    # Assert
    assert _xr.testing.assert_equal(rolling_statistic, result_array) is None
    
    
def test_execute_value_array_rolling_statistics_average():
    """RullingStatisticsRule (average, yearly)"""

    # create test set
    logger = Mock(ILogger)
    rule = RollingStatisticsRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.MEDIAN,
        time_scale="day",
        period=2,
    )

    rolling_statistic = rule.execute(value_array, logger)

    result_data = [np.nan, np.nan, 0.2, 0.2, 0.2, 0.2]
    result_array = _xr.DataArray(result_data, coords=[time], dims=["time"])

    # Assert
    assert _xr.testing.assert_equal(rolling_statistic, result_array) is None


def test_operation_type_not_implemented():
    """Test that the rulling statistics rule gives an error
    if no operation_type is given"""

    # create test set
    logger = Mock(ILogger)
    rule = RollingStatisticsRule(
        name="test",
        input_variable_names=["foo"],
        operation_type="test",
        time_scale="day",
        period=2,
    )

    with pytest.raises(NotImplementedError) as exc_info:
        rule.execute(value_array, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "The operation type 'test' is currently not supported"
    assert exception_raised.args[0] == expected_message