"""
Tests for time condition rule
"""
import numpy as np
import pytest
import xarray as _xr
from mock import Mock

# from decoimpact.business.entities.rules.time import TimeAggregationRule
from decoimpact.business.entities.rules.time_condition_rule import TimeConditionRule
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.time_operation_type import TimeOperationType

# # data_yearly = [0.0, 0.01, 3, 0.02, 0.5, 0.02]
# data_yearly = [1, 0, 1, 1, 0, 0]
# time_yearly = [
#     "2020-01-01",
#     "2020-02-02",
#     "2020-03-03",
#     "2020-04-04",
#     "2021-03-03",
#     "2021-04-04",
# ]
# time_yearly = [np.datetime64(t) for t in time_yearly]
# value_array_yearly = _xr.DataArray(data_yearly, coords=[time_yearly], dims=["time"])


# test data:
# temperature = [21, 22, 22.5, 24, 18, 19]
td_water_level = [0.0, 5, 0.001, 0, 2, 3]
td_dry = [1, 0, 1, 1, 0, 0]
td_time = [
    "2020-01-01",
    "2020-02-02",
    "2020-03-03",
    "2020-04-04",
    "2021-03-03",
    "2021-04-04",
]
td_time = [np.datetime64(t) for t in td_time]
# value_array_yearly = _xr.DataArray(data_yearly, coords=[time_yearly], dims=["time"])
ds = _xr.Dataset(
    {'water_level': ('time', td_water_level),
     'dry': ('time', td_dry)
     }, coords={
         'time': td_time
     }
)
# ds['dry']

result_time_yearly = ["2020-12-31", "2021-12-31"]
result_time_yearly = [np.datetime64(t) for t in result_time_yearly]


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


# def test_condition_time_rule_without_time_dimension():
#     """TimeConditionRule should give an error when no time dim is defined"""
#     # create test set
#     logger = Mock(ILogger)
#     rule = TimeConditionRule(
#         name="test",
#         input_variable_names=["foo"],
#         operation_type=TimeOperationType.ADD,
#     )

#     test_data = [1, 2]
#     test_array = _xr.DataArray(test_data, name="test_with_error")

#     with pytest.raises(ValueError) as exc_info:
#         rule.execute(test_array, logger)

#     exception_raised = exc_info.value

#     # Assert
#     expected_message = "No time dimension found for test_with_error"
#     assert exception_raised.args[0] == expected_message

# def test_execute_count_groups():
    """test function count_groups"""
    


def test_execute_value_array_condition_time_yearly_count_periods():
    """condition input_variable_names of a TimeConditionRule (min, yearly)"""

    # create test set
    logger = Mock(ILogger)
    rule = TimeConditionRule(
        name="test",
        operation_type='COUNT_PERIODS',
        input_variable_names=["dry"],
        output_variable_name='number_of_dry_periods',
        operation_type=TimeOperationType.COUNT_PERIODS
    )

    assert isinstance(rule, TimeConditionRule())
    time_condition = rule.execute(value_array_yearly, logger)

    result_data = [2.0, 0.0]
    result_array = _xr.DataArray(
        result_data, coords=[result_time_yearly], dims=["time_year"]
    )

    # Assert
    assert _xr.testing.assert_equal(time_condition, result_array) is None

################################################################


# data_monthly = [0, 1, 1, 0, 1]
# time_monthly = [
#     "2020-01-01",
#     "2020-02-02",
#     "2020-02-03",
#     "2020-03-04",
#     "2020-03-10",
# ]
# time_monthly = [np.datetime64(t) for t in time_monthly]
# value_array_monthly = _xr.DataArray(data_monthly, coords=[time_monthly], dims=["time"])

# result_time_monthly = [
#     "2020-01-31",
#     "2020-02-29",
#     "2020-03-31",
# ]
# result_time_monthly = [np.datetime64(t) for t in result_time_monthly]

# ####################################################################


# def test_execute_value_array_condition_time_monthly_count_periods():
#     """condition input_variable_names of a TimeConditionRule (count_periods, monthly)"""

#     # create test set
#     logger = Mock(ILogger)
#     rule = TimeConditionRule(
#         name="test",
#         input_variable_names=["foo"],
#         operation_type=TimeOperationType.COUNT_PERIODS,
#         time_scale="month",
#     )

#     time_condition = rule.execute(value_array_monthly, logger)

#     # result_data = [1, 2, 2]
#     result_data = [0, 1, 1]
#     result_array = _xr.DataArray(
#         result_data, coords=[result_time_monthly], dims=["time_month"]
#     )

#     # Assert
#     assert (
#         _xr.testing.assert_allclose(time_condition, result_array, atol=1e-11) is None
#     )


