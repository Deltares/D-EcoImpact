"""
Tests for time aggregation rule
"""
import xarray as _xr

from decoimpact.business.entities.rules.operation_type import OperationType
from decoimpact.business.entities.rules.time_aggregation_rule import TimeAggregationRule


def test_create_time_aggregation_rule_should_set_defaults():
    """Test creating a time aggregation rule with defaults"""

    # Arrange & Act
    rule = TimeAggregationRule(
        "Chloride policy per year", ["chloride_policy_top_layer"], OperationType.Min
    )

    # Assert
    assert rule.name == "Chloride policy per year"
    assert rule.description == ""
    assert rule._input_variable_names == ["chloride_policy_top_layer"]
    assert rule._output_variable_name == "output"
    assert rule._operation_type == OperationType.Min
    assert isinstance(rule, TimeAggregationRule)


def test_execute_value_array_aggregate_time():
    """Test aggregate input_variable_names of a TimeAggregationRule"""

    # Arrange & Act
    rule = TimeAggregationRule("test", ["chloride_policy_top_layer"], OperationType.Min)
    data = [1, 2, 3, 4]
    value_array = _xr.DataArray(data)
    time_aggregation = rule.execute(value_array)

    # result_data = [2.0, 4.0, 6.0, 8.0]
    result_data = []
    result_array = _xr.DataArray(result_data)

    # Assert
    assert _xr.testing.assert_equal(time_aggregation, result_array) == None
