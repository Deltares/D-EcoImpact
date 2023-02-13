"""
Tests for time aggregation rule
"""
import numpy as np
import pytest
import xarray as _xr

from decoimpact.business.entities.rules.operation_type import OperationType
from decoimpact.business.entities.rules.time_aggregation_rule import TimeAggregationRule

data = [0.1, 0.7, 0.2, 0.2, 0.3, 0.1]
time = [
    "2020-01-01",
    "2020-02-02",
    "2020-03-03",
    "2020-04-04",
    "2021-03-03",
    "2021-04-04",
]
time = [np.datetime64(t) for t in time]
value_array = _xr.DataArray(data, coords=[time], dims=["time"])


def test_create_time_aggregation_rule_should_set_defaults():
    """Test creating a time aggregation rule with defaults"""

    # Arrange & Act
    rule = TimeAggregationRule(
        "Chloride policy per year", ["chloride_policy_top_layer"], OperationType.MIN
    )

    # Assert
    assert rule.name == "Chloride policy per year"
    assert rule.description == ""
    assert isinstance(rule, TimeAggregationRule)


def test_aggregate_time_rule_without_time_dimension():
    """TimeAggregationRule should give an error when no time dim is defined"""

    # create test set
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["chloride_policy_top_layer"],
        operation_type=OperationType.MULTIPLY,
    )

    test_data = [1.2, 0.4]
    test_array = _xr.DataArray(test_data, name="test_with_error")

    with pytest.raises(ValueError) as exc_info:
        rule.execute(test_array)

    exception_raised = exc_info.value

    # Assert
    expected_message = f"No time dimension found for test_with_error"
    assert exception_raised.args[0] == expected_message


def test_execute_value_array_aggregate_time_yearly_multiply():
    """Aggregate input_variable_names of a TimeAggregationRule (MULTIPLY, yearly)"""

    # create test set
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["chloride_policy_top_layer"],
        operation_type=OperationType.MULTIPLY,
    )

    time_aggregation = rule.execute(value_array)

    result_data = [1.2, 0.4]
    result_time = ["2020-12-31", "2021-12-31"]
    result_time = [np.datetime64(t) for t in result_time]
    result_array = _xr.DataArray(result_data, coords=[result_time], dims=["time_years"])

    # Assert
    assert _xr.testing.assert_equal(time_aggregation, result_array) == None


def test_execute_value_array_aggregate_time_yearly_min():
    """Aggregate input_variable_names of a TimeAggregationRule (min, yearly)"""

    # create test set
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["chloride_policy_top_layer"],
        operation_type=OperationType.MIN,
    )

    time_aggregation = rule.execute(value_array)

    result_data = [0.1, 0.1]
    result_time = ["2020-12-31", "2021-12-31"]
    result_time = [np.datetime64(t) for t in result_time]
    result_array = _xr.DataArray(result_data, coords=[result_time], dims=["time_years"])

    # Assert
    assert _xr.testing.assert_equal(time_aggregation, result_array) == None


def test_execute_value_array_aggregate_time_yearly_max():
    """Aggregate input_variable_names of a TimeAggregationRule (MAX, yearly)"""

    # create test set
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["chloride_policy_top_layer"],
        operation_type=OperationType.MAX,
    )

    time_aggregation = rule.execute(value_array)

    result_data = [0.7, 0.3]
    result_time = ["2020-12-31", "2021-12-31"]
    result_time = [np.datetime64(t) for t in result_time]
    result_array = _xr.DataArray(result_data, coords=[result_time], dims=["time_years"])

    # Assert
    assert _xr.testing.assert_equal(time_aggregation, result_array) == None


def test_execute_value_array_aggregate_time_yearly_average():
    """Aggregate input_variable_names of a TimeAggregationRule (average, yearly)"""

    # create test set
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["chloride_policy_top_layer"],
        operation_type=OperationType.AVERAGE,
    )

    time_aggregation = rule.execute(value_array)

    result_data = [0.3, 0.2]
    result_time = ["2020-12-31", "2021-12-31"]
    result_time = [np.datetime64(t) for t in result_time]
    result_array = _xr.DataArray(result_data, coords=[result_time], dims=["time_years"])

    # Assert
    assert _xr.testing.assert_equal(time_aggregation, result_array) == None


def test_execute_value_array_aggregate_time_yearly_median():
    """Test aggregate input_variable_names of a TimeAggregationRule (median, yearly)"""

    # create test set
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["chloride_policy_top_layer"],
        operation_type=OperationType.MEDIAN,
    )

    time_aggregation = rule.execute(value_array)

    result_data = [0.2, 0.2]
    result_time = ["2020-12-31", "2021-12-31"]
    result_time = [np.datetime64(t) for t in result_time]
    result_array = _xr.DataArray(result_data, coords=[result_time], dims=["time_years"])

    # Assert
    assert _xr.testing.assert_equal(time_aggregation, result_array) == None
