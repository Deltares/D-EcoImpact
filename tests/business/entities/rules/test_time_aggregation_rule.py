# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for time aggregation rule
"""
import numpy as np
import pytest
import xarray as _xr
from mock import Mock

from decoimpact.business.entities.rules.time_aggregation_rule import TimeAggregationRule
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.time_operation_type import TimeOperationType

data_yearly = [0.1, 0.7, 0.2, 0.2, 0.3, 0.1]
time_yearly = [
    "2020-01-01",
    "2020-02-02",
    "2020-03-03",
    "2020-04-04",
    "2021-03-03",
    "2021-04-04",
]
time_yearly = [np.datetime64(t) for t in time_yearly]
value_array_yearly = _xr.DataArray(data_yearly, coords=[time_yearly], dims=["time"])

result_time_yearly = ["2020-12-31", "2021-12-31"]
result_time_yearly = [np.datetime64(t) for t in result_time_yearly]


def test_create_time_aggregation_rule_should_set_defaults():
    """Test creating a time aggregation rule with defaults"""

    # Arrange & Act
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.MIN,
    )

    # Assert
    assert rule.name == "test"
    assert rule.description == ""
    assert isinstance(rule, TimeAggregationRule)


def test_aggregate_time_rule_without_time_dimension():
    """TimeAggregationRule should give an error when no time dim is defined"""
    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.ADD,
    )

    test_data = [1.2, 0.4]
    test_array = _xr.DataArray(test_data, name="test_with_error")

    with pytest.raises(ValueError) as exc_info:
        rule.execute(test_array, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "No time dimension found for test_with_error"
    assert exception_raised.args[0] == expected_message


def test_execute_value_array_aggregate_time_yearly_add():
    """Aggregate input_variable_names of a TimeAggregationRule (add, yearly)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.ADD,
    )

    time_aggregation = rule.execute(value_array_yearly, logger)

    result_data = [1.2, 0.4]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_yearly], dims=["time_year"]
    )

    # Assert
    assert _xr.testing.assert_equal(time_aggregation, result_array) is None


def test_execute_value_array_aggregate_time_yearly_min():
    """Aggregate input_variable_names of a TimeAggregationRule (min, yearly)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.MIN,
    )

    time_aggregation = rule.execute(value_array_yearly, logger)

    result_data = [0.1, 0.1]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_yearly], dims=["time_year"]
    )

    # Assert
    assert _xr.testing.assert_equal(time_aggregation, result_array) is None


def test_execute_value_array_aggregate_time_yearly_max():
    """Aggregate input_variable_names of a TimeAggregationRule (max, yearly)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.MAX,
    )

    time_aggregation = rule.execute(value_array_yearly, logger)

    result_data = [0.7, 0.3]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_yearly], dims=["time_year"]
    )

    # Assert
    assert _xr.testing.assert_equal(time_aggregation, result_array) is None


def test_execute_value_array_aggregate_time_yearly_average():
    """Aggregate input_variable_names of a TimeAggregationRule (average, yearly)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.AVERAGE,
    )

    time_aggregation = rule.execute(value_array_yearly, logger)

    result_data = [0.3, 0.2]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_yearly], dims=["time_year"]
    )

    # Assert
    assert _xr.testing.assert_equal(time_aggregation, result_array) is None


def test_execute_value_array_aggregate_time_yearly_median():
    """Test aggregate input_variable_names of a TimeAggregationRule (median, yearly)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.MEDIAN,
    )

    time_aggregation = rule.execute(value_array_yearly, logger)

    result_data = [0.2, 0.2]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_yearly], dims=["time_year"]
    )

    # Assert
    assert _xr.testing.assert_equal(time_aggregation, result_array) is None


################################################################

data_months = [0.1, 0.7, 0.2, 0.2, 0.3]
time_months = [
    "2020-01-01",
    "2020-02-02",
    "2020-02-03",
    "2020-03-04",
    "2020-03-10",
]
time_months = [np.datetime64(t) for t in time_months]
value_array_months = _xr.DataArray(data_months, coords=[time_months], dims=["time"])

result_time_months = [
    "2020-01-31",
    "2020-02-29",
    "2020-03-31",
]
result_time_months = [np.datetime64(t) for t in result_time_months]
time_multi_year = [
    "2020-01-01",
    "2020-02-02",
    "2020-03-03",
    "2020-04-04",
    "2020-05-05",
    "2020-06-06",
    "2020-07-07",
    "2020-08-08",
    "2020-09-09",
    "2020-10-10",
    "2020-11-11",
    "2020-12-12",
    "2021-01-01",
    "2021-02-02",
    "2021-03-03",
    "2021-04-04",
    "2021-05-05",
    "2021-06-06",
    "2021-07-07",
    "2021-08-08",
    "2021-09-09",
    "2021-10-10",
    "2021-11-11",
    "2021-12-12",
]
data_multi_year = [
    0.1,
    0.7,
    0.2,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    0.2,
    0.2,
    0.4,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
]
result_time_multi_year_monthly = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
time_multi_year = [np.datetime64(t) for t in time_multi_year]
value_array_multi_year_monthly = _xr.DataArray(
    data_multi_year, coords=[time_multi_year], dims=["time"]
)

####################################################################


def test_execute_value_array_aggregate_time_months_add():
    """Aggregate input_variable_names of a TimeAggregationRule (add, monthly)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test", input_variable_names=["foo"], operation_type=TimeOperationType.ADD
    )

    rule.settings.time_scale = "month"

    time_aggregation = rule.execute(value_array_months, logger)

    result_data = [0.1, 0.9, 0.5]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_months], dims=["time_month"]
    )

    # Assert
    assert (
        _xr.testing.assert_allclose(time_aggregation, result_array, atol=1e-11) is None
    )


def test_execute_value_array_aggregate_time_months_min():
    """Aggregate input_variable_names of a TimeAggregationRule (min, monthly)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.MIN,
    )
    rule.settings.time_scale = "month"

    time_aggregation = rule.execute(value_array_months, logger)

    result_data = [0.1, 0.2, 0.2]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_months], dims=["time_month"]
    )

    # Assert
    assert _xr.testing.assert_equal(time_aggregation, result_array) is None


def test_execute_value_array_aggregate_time_months_max():
    """Aggregate input_variable_names of a TimeAggregationRule (max, months)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.MAX,
    )
    rule.settings.time_scale = "month"

    time_aggregation = rule.execute(value_array_months, logger)

    result_data = [0.1, 0.7, 0.3]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_months], dims=["time_month"]
    )

    # Assert
    assert (
        _xr.testing.assert_equal(
            time_aggregation,
            result_array,
        )
        is None
    )


def test_execute_value_array_aggregate_time_months_average():
    """Aggregate input_variable_names of a TimeAggregationRule (average, months)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.AVERAGE,
    )
    rule.settings.time_scale = "month"

    time_aggregation = rule.execute(value_array_months, logger)

    result_data = [0.1, 0.45, 0.25]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_months], dims=["time_month"]
    )

    # Assert
    assert (
        _xr.testing.assert_allclose(time_aggregation, result_array, atol=1e-11) is None
    )


def test_execute_value_array_aggregate_time_months_median():
    """Test aggregate input_variable_names of a TimeAggregationRule (median, months)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.MEDIAN,
    )
    rule.settings.time_scale = "month"

    time_aggregation = rule.execute(value_array_months, logger)

    result_data = [0.1, 0.45, 0.25]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_months], dims=["time_month"]
    )

    # Assert
    assert (
        _xr.testing.assert_allclose(time_aggregation, result_array, atol=1e-11) is None
    )


def test_execute_value_array_aggregate_time_months_stdev():
    """Test aggregate input_variable_names of a TimeAggregationRule
    (STDEV, months)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.STDEV,
    )
    rule.settings.time_scale = "month"

    time_aggregation = rule.execute(value_array_months, logger)
    result_data = [0.0, 0.25, 0.05]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_months], dims=["time_month"]
    )

    # Assert
    assert (
        _xr.testing.assert_allclose(time_aggregation, result_array, atol=1e-11) is None
    )


def test_execute_value_array_aggregate_time_months_percentile():
    """Test aggregate input_variable_names of a TimeAggregationRule
    (PERCENTILE, months)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.PERCENTILE,
    )
    rule.settings.time_scale = "month"
    rule.settings.percentile_value = 10

    time_aggregation = rule.execute(value_array_months, logger)
    result_data = [0.1, 0.25, 0.21]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_months], dims=["time_month"]
    )

    # Assert
    assert (
        _xr.testing.assert_allclose(time_aggregation, result_array, atol=1e-11) is None
    )


def test_multi_year_monthly_average():
    """Aggregate input_variable_names of a TimeAggregationRule (average, months)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.MULTI_YEAR_MONTHLY_AVERAGE,
    )
    rule.settings.time_scale = "month"

    time_aggregation = rule.execute(value_array_multi_year_monthly, logger)

    result_data = [0.15, 0.45, 0.3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_multi_year_monthly], dims=["time_monthly"]
    )

    # Assert
    assert (
        _xr.testing.assert_allclose(time_aggregation, result_array, atol=1e-11) is None
    )


def test_multi_yearly_month_average_with_year_range():
    """Aggregate input_variable_names of a TimeAggregationRule (average, months) with year range"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.MULTI_YEAR_MONTHLY_AVERAGE,
        start_year=2020,
        end_year=2020,
    )
    rule.settings.time_scale = "month"

    time_aggregation = rule.execute(value_array_multi_year_monthly, logger)

    result_data = [0.1, 0.7, 0.2, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_multi_year_monthly], dims=["time_monthly"]
    )

    # Assert
    assert (
        _xr.testing.assert_allclose(time_aggregation, result_array, atol=1e-11) is None
    )


def test_operation_type_not_implemented():
    """Test that the time aggregation rule gives an error
    if no operation_type is given"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type="test",
    )
    rule.settings.time_scale = "month"

    with pytest.raises(NotImplementedError) as exc_info:
        rule.execute(value_array_months, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "The operation type 'test' is currently not supported"
    assert exception_raised.args[0] == expected_message
