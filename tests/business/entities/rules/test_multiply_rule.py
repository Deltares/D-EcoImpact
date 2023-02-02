"""
Tests for RuleBase class
"""


import xarray as _xr

from decoimpact.business.entities.rules.multiply_rule import MultiplyRule


def test_create_multiply_rule_should_set_defaults():
    """Test creating a RuleBase with defaults"""

    # Arrange & Act
    rule = MultiplyRule("test", ["foo"], [0.5, 3.0])
    # Assert
    assert rule.name == "test"
    assert rule.description == ""
    assert rule._input_variable_names == ["foo"]
    assert rule._output_variable_name == "output"
    assert rule._multipliers == [0.5, 3.0]
    assert isinstance(rule, MultiplyRule)


def test_setting_name_of_rule():
    """Test setting name of a RuleBase"""

    # Arrange & Act
    rule = MultiplyRule("test", ["foo"], [0.5, 3.0])

    # Assert
    assert rule.name == "test"
    rule.name = "foo"
    assert rule.name == "foo"


def test_setting_description_of_rule():
    """Test setting description of a RuleBase"""

    # Arrange & Act
    rule = MultiplyRule("test", ["foo"], [0.5, 3.0])

    # Assert
    assert rule.description == ""
    rule.description = "foo"
    assert rule.description == "foo"


def test_setting_input_variable_names_of_rule():
    """Test setting input_variable_names of a RuleBase"""

    # Arrange & Act
    rule = MultiplyRule("test", ["foo"], [0.5, 3.0])

    # Assert
    assert rule.input_variable_names == ["foo"]
    rule.input_variable_names = ["foo", "bar"]
    assert rule.input_variable_names == ["foo", "bar"]


def test_setting_output_variable_name_of_rule():
    """Test setting input_variable_names of a RuleBase"""

    # Arrange & Act
    rule = MultiplyRule("test", ["foo"], [0.5, 3.0])

    # Assert
    assert rule.output_variable_name == "output"
    rule.output_variable_name = "foo"
    assert rule.output_variable_name == "foo"


def test_execute_value_array_multiplied_by_multipliers():
    """Test setting input_variable_names of a RuleBase"""

    # Arrange & Act
    rule = MultiplyRule("test", ["foo"], [0.5, 4.0])
    data = [1, 2, 3, 4]
    value_array = _xr.DataArray(data)
    multiplied_array = rule.execute(value_array)

    result_data = [2.0, 4.0, 6.0, 8.0]
    result_array = _xr.DataArray(result_data)

    # Assert
    assert _xr.testing.assert_equal(multiplied_array, result_array) == None
