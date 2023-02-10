"""
Tests for LayerFilterRule class
"""
import xarray as _xr

from decoimpact.business.entities.rules.layer_filter_rule import LayerFilterRule


def test_create_layer_filter_rule_should_set_defaults():
    """Test creating a LayerFilterRule with defaults"""

    # Arrange & Act
    rule = LayerFilterRule("test", ["foo"], 3, "output")

    # Assert
    assert rule.name == "test"
    assert rule.description == ""
    assert rule.input_variable_names == ["foo"]
    assert rule.output_variable_name == "output"
    assert rule.layer_number == 3
    assert isinstance(rule, LayerFilterRule)


def test_execute_value_array_filtered():
    """Test execute of layer filter rule"""
    # Arrange & Act
    rule = LayerFilterRule("test", ["foo"], 3, "output", "description")
    data = [[[1, 2, 3, 4]]]
    value_array = _xr.DataArray(data)
    filtered_array = rule.execute(value_array)

    result_data = [[3]]
    result_array = _xr.DataArray(result_data)

    # Assert
    assert _xr.testing.assert_equal(filtered_array, result_array) is None
