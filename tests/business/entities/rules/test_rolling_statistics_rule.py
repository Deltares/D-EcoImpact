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

from decoimpact.business.entities.rules.rolling_statistic_rule import (
    RollingStatisticRule,
)
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.time_operation_type import TimeOperationType

data_yearly = [0.1, 0.7, 0.2, 0.2, 0.3, 0.1]
time_yearly = [
    "2020-01-01",
    "2020-02-02",
    "2020-03-03",
    "2020-04-04",
    "2021-01-01",
    "2021-03-01",
]
time_yearly = [np.datetime64(t) for t in time_yearly]
value_array_yearly = _xr.DataArray(data_yearly, coords=[time_yearly], dims=["time"])

result_time_yearly = ["2020-12-31", "2021-12-31"]
result_time_yearly = [np.datetime64(t) for t in result_time_yearly]


def test_create_rolling_statistics_rule_should_set_defaults():
    """Test creating a rolling statistics rule with defaults"""

    # Arrange & Act
    rule = RollingStatisticRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.MIN,
    )

    # Assert
    assert rule.name == "test"
    assert rule.description == ""
    assert isinstance(rule, RollingStatisticRule)


def test_rolling_statistics_rule_without_time_dimension():
    """RollingStatisticsRule should give an error when no time dim is defined"""
    # create test set
    logger = Mock(ILogger)
    rule = RollingStatisticRule(
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
    """Aggregate input_variable_names of a TimeAggregationRule (max, yearly)"""

    # create test set
    logger = Mock(ILogger)
    rule = RollingStatisticRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.MAX,
        time_scale="day",
        period=365,
    )

    time_aggregation = rule.execute(value_array_yearly, logger)

    result_data = [np.nan, np.nan, np.nan, 0.7, 0.7, np.nan]
    # result: array([nan, nan, nan, 0.7, 0.7, nan])
    result_array = _xr.DataArray(result_data, coords=[time_yearly], dims=["time"])

    # Assert
    assert _xr.testing.assert_equal(time_aggregation, result_array) is None
