# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the 
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for time aggregation rule
for operation types:
 - COUNT_PERIODS
 - MAX_DURATION_PERIODS
 - AVG_DURATION_PERIODS
"""
import numpy as _np
import pytest
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
    assert rule.operation_type == TimeOperationType.COUNT_PERIODS
    assert rule.time_scale == "year"
    assert rule.time_scale_mapping == {"month": "M", "year": "Y"}


def test_validation_when_valid():
    """Test if the rule is validated properly"""
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.COUNT_PERIODS,
        time_scale="month"
    )

    valid = rule.validate(logger)
    assert valid


def test_validation_when_not_valid():
    """Test if the rule is validated properly"""
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.COUNT_PERIODS,
        time_scale="awhile"
    )

    valid = rule.validate(logger)
    allowed_time_scales = rule._time_scale_mapping.keys()
    options = ",".join(allowed_time_scales)
    logger.log_error.assert_called_with(
        f"The provided time scale '{rule.time_scale}' "
        f"of rule '{rule.name}' is not supported.\n"
        f"Please select one of the following types: "
        f"{options}"
    )
    assert not valid


def test_analyze_groups_function_not_only_1_and_0():
    """Test whether it gives an error if the data array contains
    other values than 0 and 1"""
    logger = Mock(ILogger)
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType.COUNT_PERIODS,
    )
    t_data = [2, 3, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1]
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

    # Act
    with pytest.raises(ValueError) as exc_info:
        rule.execute(input_array, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = (
        "The value array for the time aggregation rule with operation type"
        " COUNT_PERIODS should only contain the values 0 and 1."
    )
    assert exception_raised.args[0] == expected_message


@pytest.mark.parametrize(
    "operation_type, expected_result_data",
    [
        ("COUNT_PERIODS", [2, 2, 2, 2]),
        ("MAX_DURATION_PERIODS", [2, 2, 3, 3]),
        ("AVG_DURATION_PERIODS", [1.5, 1.5, 2, 2])
    ],
)
def test_analyze_groups_function(operation_type, expected_result_data):
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
        operation_type=TimeOperationType[operation_type],
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
    result = input_array.resample(time="Y").reduce(rule.analyze_groups)

    # expected results
    expected_result_time = ["2000-12-31", "2001-12-31", "2002-12-31", "2003-12-31"]
    expected_result_time = [_np.datetime64(t) for t in expected_result_time]
    expected_result = _xr.DataArray(
        expected_result_data, coords=[expected_result_time], dims=["time"]
    )

    assert _xr.testing.assert_equal(expected_result, result) is None


@pytest.mark.parametrize(
    "operation_type, expected_result_data",
    [
        ("COUNT_PERIODS", [0, 1, 0, 0]),
        ("MAX_DURATION_PERIODS", [0, 1, 0, 0]),
        ("AVG_DURATION_PERIODS", [0, 1, 0, 0])
    ],
)
def test_analyze_groups_function_no_periods(operation_type, expected_result_data):
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
        operation_type=TimeOperationType[operation_type],
    )
    t_data = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
    result = input_array.resample(time="Y").reduce(rule.analyze_groups)

    # expected results
    expected_result_time = ["2000-12-31", "2001-12-31", "2002-12-31", "2003-12-31"]
    expected_result_time = [_np.datetime64(t) for t in expected_result_time]
    expected_result = _xr.DataArray(
        expected_result_data, coords=[expected_result_time], dims=["time"]
    )

    assert _xr.testing.assert_equal(expected_result, result) is None


@pytest.mark.parametrize(
    "operation_type, expected_result_data",
    [
        ("COUNT_PERIODS", [[2, 2, 2, 2], [1, 2, 2, 2], [2, 1, 2, 2]]),
        ("MAX_DURATION_PERIODS", [[2, 2, 3, 3], [1, 2, 3, 3], [2, 2, 3, 3]]),
        ("AVG_DURATION_PERIODS", [[1.5, 1.5, 2, 2], [1, 1.5, 2, 2], [1.5, 2, 2, 2]])
    ],
)
def test_analyze_groups_function_2d(operation_type, expected_result_data):
    """Test if functional for 2d arrays"""
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType[operation_type],
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
    t_cells = [0, 1, 2]
    input_array = _xr.DataArray(
        t_data, coords=[t_cells, t_time], dims=["cells", "time"]
    )
    result = input_array.resample(time="Y").reduce(rule.analyze_groups)

    # expected results
    expected_result_time = ["2000-12-31", "2001-12-31", "2002-12-31", "2003-12-31"]
    expected_result_time = [_np.datetime64(t) for t in expected_result_time]
    expected_result = _xr.DataArray(
        expected_result_data,
        coords=[t_cells, expected_result_time],
        dims=["cells", "time"],
    )

    assert _xr.testing.assert_equal(expected_result, result) is None


@pytest.mark.parametrize(
    "operation_type, expected_result_data",
    [
        ("COUNT_PERIODS", [
            [[2, 2, 2, 2], [1, 2, 2, 2], [2, 1, 2, 2]],
            [[2, 2, 2, 2], [1, 2, 2, 2], [2, 1, 2, 2]]
        ]),
        ("MAX_DURATION_PERIODS", [
            [[2, 2, 3, 3], [1, 2, 3, 3], [2, 2, 3, 3]],
            [[2, 2, 3, 3], [1, 2, 3, 3], [2, 2, 3, 3]]
        ]),
        ("AVG_DURATION_PERIODS", [
            [[1.5, 1.5, 2, 2], [1, 1.5, 2, 2], [1.5, 2, 2, 2]],
            [[1.5, 1.5, 2, 2], [1, 1.5, 2, 2], [1.5, 2, 2, 2]]
        ], )
    ],
)
def test_count_groups_function_3d(operation_type, expected_result_data):
    """Test if functional for multiple dimensions"""
    rule = TimeAggregationRule(
        name="test",
        input_variable_names=["foo"],
        operation_type=TimeOperationType[operation_type],
    )

    t_data = [[
        [0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    ], [
        [0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    ]]
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
    t_cells = [0, 1, 2]
    t_cols = [0, 1]
    input_array = _xr.DataArray(
        t_data, coords=[t_cols, t_cells, t_time], dims=["cols", "cells", "time"]
    )
    result = input_array.resample(time="Y").reduce(rule.analyze_groups)

    # expected results
    expected_result_time = ["2000-12-31", "2001-12-31", "2002-12-31", "2003-12-31"]
    expected_result_time = [_np.datetime64(t) for t in expected_result_time]
    expected_result = _xr.DataArray(
        expected_result_data,
        coords=[t_cols, t_cells, expected_result_time],
        dims=["cols", "cells", "time"],
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
