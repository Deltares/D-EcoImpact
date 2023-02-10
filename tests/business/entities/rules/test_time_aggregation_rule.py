"""
Tests for time aggregation rule
"""
from unittest import result

import pandas as pd
import xarray as _xr

from decoimpact.business.entities.rules.operation_type import OperationType
from decoimpact.business.entities.rules.time_aggregation_rule import TimeAggregationRule


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


# def test_execute_value_array_aggregate_time():
#     """Test aggregate input_variable_names of a TimeAggregationRule"""

#     # create test set
#     # operation_min = OperationType.Min
#     rule = TimeAggregationRule("test", ["chloride_policy_top_layer"], OperationType.MIN)
#     data = [1, 2, 3]
#     time = pd.date_range(start="2020-01-01", end="2020-03-01", periods=3)
#     ds_values = _xr.Dataset(
#         data_vars=dict(data=(["time"], data)), coords=dict(time=time)
#     )
#     value_array = ds_values.to_array()
#     time_aggregation = rule.execute(value_array)

#     # create result set
#     data = [1]
#     time = pd.date_range("2020-01-01", periods=1)
#     ds_result = _xr.Dataset(
#         data_vars=dict(data=(["time"], data)), coords=dict(time=time)
#     )
#     result_array = ds_result.to_array()
#     print('result_arraw', result_array)

#     # Assert
#     assert _xr.testing.assert_equal(time_aggregation, result_array) == None
