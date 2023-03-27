"""
Tests for RuleBase class
"""


from unittest.mock import Mock

import numpy as _np
import pytest
import xarray as _xr

from decoimpact.business.entities.rules.response_rule import ResponseRule
from decoimpact.crosscutting.i_logger import ILogger


@pytest.fixture
def example_rule():
    return ResponseRule(
        "test_response_name",
        "input_variable_name",
        [0, 50, 300, 5000],
        [0, 1, 2, 3],
    )


def test_create_response_rule(example_rule):
    """
    Test creating a new (valid) Response rule
    """
    # Arrange
    logger = Mock(ILogger)

    # Assert
    assert example_rule._name == "test_response_name"
    assert example_rule.input_variable_names[0] == "input_variable_name"
    assert (example_rule._input_values == [0, 50, 300, 5000]).all()
    assert (example_rule._output_values == [0, 1, 2, 3]).all()
    assert isinstance(example_rule, ResponseRule)
    assert example_rule.validate(logger)


@pytest.mark.parametrize(
    "input_value, expected_output_value",
    [(25, 0.5), (75, 1.1), (770, 2.1)],
)
def test_execute_response_rule_values_between_limits(
    example_rule: ResponseRule, input_value: int, expected_output_value: float
):
    """
    Test the function execution with input values between the interval limits.
    """
    # Arrange
    logger = Mock(ILogger)

    # Assert
    assert example_rule.execute(input_value, logger) == expected_output_value
    logger.log_warning.assert_not_called()


@pytest.mark.parametrize(
    "input_value, expected_log_message",
    [
        (-1, "value less than min"),
        (6000, "value greater than max"),
    ],
)
def test_execute_response_rule_values_outside_limits(
    example_rule: ResponseRule, input_value: int, expected_log_message: str
):
    """
    Test the function execution with input values outside the interval limits.
    """
    # Arrange
    logger = Mock(ILogger)

    # Assert
    assert _np.isnan(example_rule.execute(input_value, logger))
    logger.log_warning.assert_called_with(expected_log_message)


def test_inputs_and_outputs_have_different_lengths(example_rule: ResponseRule):
    """
    Test the function execution when input and outputs have different lengths
    """
    # Arrange
    logger = Mock(ILogger)

    # Act
    example_rule._input_values = _np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    # Assert
    assert not example_rule.validate(logger)
    logger.log_error.assert_called_with("The input and output values must be equal.")
