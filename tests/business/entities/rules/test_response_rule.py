"""
Tests for RuleBase class
"""


from unittest.mock import Mock

import numpy as _np
import pytest

from decoimpact.business.entities.rules.response_rule import ResponseRule
from decoimpact.crosscutting.i_logger import ILogger


@pytest.fixture(name="example_rule")
def fixture_example_rule():
    """Inititaion of ResponseRule to be reused in the following tests"""
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
    assert example_rule.name == "test_response_name"
    assert example_rule.input_variable_names[0] == "input_variable_name"
    assert (example_rule.input_values == [0, 50, 300, 5000]).all()
    assert (example_rule.output_values == [0, 1, 2, 3]).all()
    assert isinstance(example_rule, ResponseRule)
    assert example_rule.validate(logger)


@pytest.mark.parametrize(
    "input_value, expected_output_value",
    [(25, 0.5), (75, 1.1), (770, 2.1)],
)
def test_execute_response_rule_values_between_limits(
    example_rule, input_value: int, expected_output_value: float
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
    "input_value, expected_output_value, expected_log_message",
    [
        (-1, 0, "value less than min"),
        (6000, 3, "value greater than max"),
    ],
)
def test_execute_response_rule_values_outside_limits(
    example_rule,
    input_value: int,
    expected_output_value: int,
    expected_log_message: str,
):
    """
    Test the function execution with input values outside the interval limits.
    """
    # Arrange
    logger = Mock(ILogger)

    # Assert
    assert example_rule.execute(input_value, logger) == expected_output_value
    logger.log_warning.assert_called_with(expected_log_message)


def test_inputs_and_outputs_have_different_lengths(example_rule):
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


def test_input_values_are_not_sorted(example_rule):
    """
    Test the function execution when input values are not sorted
    """
    # Arrange
    logger = Mock(ILogger)

    # Act
    example_rule._input_values = _np.array([1, 2, 5, 3])

    # Assert
    assert not example_rule.validate(logger)
    logger.log_error.assert_called_with(
        "The input values should be given in a sorted order."
    )


@pytest.fixture(name="example_rule_combined")
def fixture_example_rule_combined():
    return ResponseRule(
        "name",
        "input_variable_name",
        [0, 1, 2, 5, 10],
        [22, 15, 10, 12, 20],
    )


@pytest.mark.parametrize(
    "input_value, expected_output_value",
    [(-1, 22), (0.5, 18.5), (1.5, 12.5), (3.5, 11), (7.5, 16), (10.5, 20)],
)
def test_execute_values_combined_dec_inc(
    example_rule_combined,
    input_value: int,
    expected_output_value: int,
):
    """
    Test the function execution with input values between the interval limits.
    """
    # Arrange
    logger = Mock(ILogger)

    # Assert
    assert example_rule_combined.execute(input_value, logger) == expected_output_value