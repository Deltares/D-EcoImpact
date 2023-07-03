"""
Tests for time condition rule
"""
import numpy as np
import pytest
import xarray as _xr
from mock import Mock

from decoimpact.business.entities.rules.time_condition_rule import TimeConditionRule
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.time_operation_type import TimeOperationType

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
td_time = [np.datetime64(t) for t in td_time]
test_dataset_yearly = _xr.Dataset(
    {'water_level': ('time', td_water_level),
     'dry': ('time', td_dry)
     }, coords={
         'time': td_time
     }
)
test_array_yearly = test_dataset_yearly['dry']
result_time_yearly = ["2020-12-31", "2021-12-31", "2022-12-31"]
result_time_yearly = [np.datetime64(t) for t in result_time_yearly]
result_data_yearly = [2.0, 0.0, 1.0]
################################################################


def test_create_time_condition_rule_should_set_defaults():
    """Test creating a time condition rule with defaults"""

    # Arrange & Act
    rule = TimeConditionRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.COUNT_PERIODS,
    )

    # Assert
    assert rule.name == "test"
    assert rule.description == ""
    assert isinstance(rule, TimeConditionRule)


def test_time_condition_rule_without_time_dimension():
    """TimeConditionRule should give an error when no time dim is defined"""
    # create test set
    logger = Mock(ILogger)
    rule = TimeConditionRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.ADD,
    )

    test_data_without_time = [1, 2]
    test_array_without_time = _xr.DataArray(test_data_without_time,
                                            name="test_with_error")

    with pytest.raises(ValueError) as exc_info:
        rule.execute(test_array_without_time, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "No time dimension found for test_with_error"
    assert exception_raised.args[0] == expected_message

# TODO: test count_periods-function
# def test_simple_count_periods_function():
#     """test function to count periods with simple example"""
#     rule = TimeConditionRule(
#         name="test",
#         input_variable_names=["foo"],
#         operation_type=TimeOperationType.ADD,
#     )

#     test_agg_val = ....
#     result = test_agg_val.reduce(rule.count_periods)
#     expected_result = [...,...]
#     assert _xr.testing.assert_equal(expected_result, result) is None

def test_execute_value_array_condition_time_yearly_count_periods():
    """condition input_variable_names of a TimeConditionRule (min, yearly)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeConditionRule(
        name="test",
        input_variable_names=["dry"],
        operation_type=TimeOperationType.COUNT_PERIODS,
        output_variable_name='number_of_dry_periods'
        )

    assert isinstance(rule, TimeConditionRule)
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
time_monthly = [np.datetime64(t) for t in time_monthly]
value_array_monthly = _xr.DataArray(data_monthly, coords=[time_monthly], dims=["time"])
result_time_monthly = [
    "2020-01-31",
    "2020-02-29",
    "2020-03-31",
]
result_time_monthly = [np.datetime64(t) for t in result_time_monthly]
####################################################################


def test_execute_value_array_condition_time_monthly_count_periods():
    """condition input_variable_names of a TimeConditionRule (count_periods, monthly)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeConditionRule(
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
    assert (
        _xr.testing.assert_allclose(time_condition, result_array, atol=1e-11) is None
    )
