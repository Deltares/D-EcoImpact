"""
Tests for RuleBase class
"""


from unittest.mock import Mock

import xarray as _xr

from decoimpact.business.entities.rules.multiply_rule import MultiplyRule
from decoimpact.crosscutting.i_logger import ILogger


def test_create_multiply_rule_should_set_defaults():
    """Test creating a RuleBase with defaults"""

    # Arrange & Act
    rule = MultiplyRule("test", ["foo"], [0.5, 3.0])
    # Assert
    assert rule.name == "test"
    assert rule.description == ""
    assert rule.input_variable_names == ["foo"]
    assert rule.output_variable_name == "output"
    assert rule.multipliers == [0.5, 3.0]
    assert isinstance(rule, MultiplyRule)


def test_execute_value_array_multiplied_by_multipliers():
    """Test setting input_variable_names of a RuleBase"""

    # Arrange
    logger = Mock(ILogger)
    rule = MultiplyRule("test", ["foo"], [0.5, 4.0], "description")
    data = [1, 2, 3, 4]
    value_array = _xr.DataArray(data)

    # Act
    multiplied_array = rule.execute(value_array, logger)

    result_data = [2.0, 4.0, 6.0, 8.0]
    result_array = _xr.DataArray(result_data)

    # Assert
    assert _xr.testing.assert_equal(multiplied_array, result_array) == None
