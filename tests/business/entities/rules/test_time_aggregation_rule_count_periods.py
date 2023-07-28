"""
Tests for time aggregation rule
"""
import numpy as _np
import xarray as _xr
from mock import Mock

from decoimpact.business.entities.rules.time_aggregation_rule import TimeAggregationRule
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.time_operation_type import TimeOperationType


def test_create_time_aggregation_rule_should_set_defaults():
    """Test creating a time aggregation rule with defaults"""

    # Arrange & Act
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.COUNT_PERIODS,
    )

    # Assert
    assert rule.name == "test"
    assert rule.description == ""
    assert isinstance(rule, TimeAggregationRule)


def test_count_groups_function():
    """Test the count_groups to count groups for several examples.

    This function is being used when 'count_periods' is given
      as aggregation in the TimeAggregationRule.
    The result should be aggregated per year.
    The count_periods should result in a number of the groups with value 1.
    This test should show that the count_periods accounts for begin and end of the year.
    """
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.COUNT_PERIODS,
    )
    t_data = [0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1]
    t_time = [
        "2000-01-01",
        "2000-01-02",
        "2000-01-03",
        "2000-01-04",
        "2000-01-05",
        "2001-01-01",
        "2001-01-02",
        "2001-01-03",
        "2001-01-04",
        "2001-01-05",
        "2002-01-01",
        "2002-01-02",
        "2002-01-03",
        "2002-01-04",
        "2002-01-05",
        "2003-01-01",
        "2003-01-02",
        "2003-01-03",
        "2003-01-04",
        "2003-01-05",
    ]
    t_time = [_np.datetime64(t) for t in t_time]
    input_array = _xr.DataArray(t_data, coords=[t_time], dims=["time"])
    result = input_array.resample(time="Y").reduce(rule.count_groups)

    # expected results
    expected_result_time = ["2000-12-31", "2001-12-31", "2002-12-31", "2003-12-31"]
    expected_result_time = [_np.datetime64(t) for t in expected_result_time]
    expected_result_data = [2, 2, 2, 2]
    expected_result = _xr.DataArray(
        expected_result_data, coords=[expected_result_time], dims=["time"]
    )

    assert _xr.testing.assert_equal(expected_result, result) is None


def test_count_groups_function_nd():
    """Test the count_groups to count groups for several examples.

    This function is being used when 'count_periods' is given
      as aggregation in the TimeAggregationRule.
    The result should be aggregated per year.
    The count_periods should result in a number of the groups with value 1.
    This test should show that the count_periods accounts for begin and end of the year.
    """
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.COUNT_PERIODS,
    )

    t_data = [
        [0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    ]
    t_time = [
        "2000-01-01",
        "2000-01-02",
        "2000-01-03",
        "2000-01-04",
        "2000-01-05",
        "2000-01-06",
        "2001-01-02",
        "2001-01-03",
        "2001-01-04",
        "2001-01-05",
        "2002-01-01",
        "2002-01-02",
        "2002-01-03",
        "2002-01-04",
        "2002-01-05",
        "2003-01-01",
        "2003-01-02",
        "2003-01-03",
        "2003-01-04",
        "2003-01-05",
    ]
    t_time = [_np.datetime64(t) for t in t_time]
    t_cells = [0, 1, 2]
    input_array = _xr.DataArray(
        t_data, coords=[t_cells, t_time], dims=["cells", "time"]
    )
    result = input_array.resample(time="Y").reduce(rule.count_groups)

    # expected results
    expected_result_time = ["2000-12-31", "2001-12-31", "2002-12-31", "2003-12-31"]
    expected_result_time = [_np.datetime64(t) for t in expected_result_time]
    expected_result_data = [
        [2, 1, 2, 2],
        [2, 1, 2, 2],
        [2, 1, 2, 2],
    ]
    expected_result = _xr.DataArray(
        expected_result_data,
        coords=[t_cells, expected_result_time],
        dims=["cells", "time"],
    )

    assert _xr.testing.assert_equal(expected_result, result) is None


################################################################
# test data yearly:
temperature = [21, 22, 22.5, 24, 18, 19, 15, 14]
td_water_level = [0.0, 5, 0.001, 0, 2, 3, 4, 4]
td_dry = [1, 0, 1, 1, 0, 0, 1, 1]
td_time = [
    "2020-01-01",
    "2020-02-02",
    "2020-03-03",
    "2020-03-04",
    "2021-03-03",
    "2021-04-04",
    "2022-11-11",
    "2022-12-12",
]
td_time = [_np.datetime64(t) for t in td_time]
test_dataset_yearly = _xr.Dataset(
    {"water_level": ("time", td_water_level), "dry": ("time", td_dry)},
    coords={"time": td_time},
)
test_array_yearly = test_dataset_yearly["dry"]
result_time_yearly = ["2020-12-31", "2021-12-31", "2022-12-31"]
result_time_yearly = [_np.datetime64(t) for t in result_time_yearly]
result_data_yearly = [2.0, 0.0, 1.0]
################################################################


def test_execute_value_array_condition_time_yearly_count_periods():
    """Test the TimeAggregationRule to count periods per year"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["dry"],
        operation_type=TimeOperationType.COUNT_PERIODS,
        output_variable_name="number_of_dry_periods",
    )

    assert isinstance(rule, TimeAggregationRule)
    time_condition = rule.execute(test_array_yearly, logger)

    result_array = _xr.DataArray(
        result_data_yearly, coords=[result_time_yearly], dims=["time_year"]
    )

    # Assert
    assert _xr.testing.assert_equal(time_condition, result_array) is None


################################################################
# test data monthly:
data_monthly = [0, 1, 1, 0, 1]
time_monthly = [
    "2020-01-01",
    "2020-02-02",
    "2020-02-03",
    "2020-03-04",
    "2020-03-10",
]
time_monthly = [_np.datetime64(t) for t in time_monthly]
value_array_monthly = _xr.DataArray(data_monthly, coords=[time_monthly], dims=["time"])
result_time_monthly = [
    "2020-01-31",
    "2020-02-29",
    "2020-03-31",
]
result_time_monthly = [_np.datetime64(t) for t in result_time_monthly]
####################################################################


def test_execute_value_array_condition_time_monthly_count_periods():
    """Test the TimeAggregationRule to count periods per month"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.COUNT_PERIODS,
        time_scale="month",
    )

    time_condition = rule.execute(value_array_monthly, logger)

    result_data = [0, 1, 1]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_monthly], dims=["time_month"]
    )

    # Assert
    assert _xr.testing.assert_equal(time_condition, result_array) is None
