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

data_monthly = [0.1, 0.7, 0.2, 0.2, 0.3]
time_monthly = [
    "2020-01-01",
    "2020-02-02",
    "2020-02-03",
    "2020-03-04",
    "2020-03-10",
]
time_monthly = [np.datetime64(t) for t in time_monthly]
value_array_monthly = _xr.DataArray(data_monthly, coords=[time_monthly], dims=["time"])

result_time_monthly = [
    "2020-01-31",
    "2020-02-29",
    "2020-03-31",
]
result_time_monthly = [np.datetime64(t) for t in result_time_monthly]

####################################################################


def test_execute_value_array_aggregate_time_monthly_add():
    """Aggregate input_variable_names of a TimeAggregationRule (add, monthly)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.ADD,
        time_scale="month",
    )

    time_aggregation = rule.execute(value_array_monthly, logger)

    result_data = [0.1, 0.9, 0.5]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_monthly], dims=["time_month"]
    )

    # Assert
    assert (
        _xr.testing.assert_allclose(time_aggregation, result_array, atol=1e-11) is None
    )


def test_execute_value_array_aggregate_time_monthly_min():
    """Aggregate input_variable_names of a TimeAggregationRule (min, monthly)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        time_scale="month",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.MIN,
    )

    time_aggregation = rule.execute(value_array_monthly, logger)

    result_data = [0.1, 0.2, 0.2]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_monthly], dims=["time_month"]
    )

    # Assert
    assert _xr.testing.assert_equal(time_aggregation, result_array) is None


def test_execute_value_array_aggregate_time_monthly_max():
    """Aggregate input_variable_names of a TimeAggregationRule (max, monthly)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        time_scale="month",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.MAX,
    )

    time_aggregation = rule.execute(value_array_monthly, logger)

    result_data = [0.1, 0.7, 0.3]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_monthly], dims=["time_month"]
    )

    # Assert
    assert (
        _xr.testing.assert_equal(
            time_aggregation,
            result_array,
        )
        is None
    )


def test_execute_value_array_aggregate_time_monthly_average():
    """Aggregate input_variable_names of a TimeAggregationRule (average, monthly)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        time_scale="month",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.AVERAGE,
    )

    time_aggregation = rule.execute(value_array_monthly, logger)

    result_data = [0.1, 0.45, 0.25]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_monthly], dims=["time_month"]
    )

    # Assert
    assert (
        _xr.testing.assert_allclose(time_aggregation, result_array, atol=1e-11) is None
    )


def test_execute_value_array_aggregate_time_monthly_median():
    """Test aggregate input_variable_names of a TimeAggregationRule (median, monthly)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        time_scale="month",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.MEDIAN,
    )

    time_aggregation = rule.execute(value_array_monthly, logger)

    result_data = [0.1, 0.45, 0.25]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_monthly], dims=["time_month"]
    )

    # Assert
    assert (
        _xr.testing.assert_allclose(time_aggregation, result_array, atol=1e-11) is None
    )


def test_operation_type_not_implemented():
    """Test that the time aggregation rule gives an error if no operation_type is given"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        time_scale="month",
        input_variable_names=["foo"],
        operation_type="test"
    )

    with pytest.raises(NotImplementedError) as exc_info:
        rule.execute(value_array_monthly, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = (
        "The operation type 'test' is currently not supported"
    )
    assert exception_raised.args[0] == expected_message
