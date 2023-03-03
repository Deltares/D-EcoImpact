"""
Tests for Step Function Rule class
"""


import numpy as _np
import pytest
from mock import Mock

from decoimpact.business.entities.rules.step_function_rule import StepFunctionRule
from decoimpact.crosscutting.i_logger import ILogger


@pytest.fixture
def example_rule():
    return StepFunctionRule(
        "step_function_rule_name",
        "input_variable_name",
        [0, 1, 2, 5, 10],
        [10, 11, 12, 15, 20],
    )


def test_create_step_function(example_rule):
    """
    Test creating a new (valid) Step Fuction rule
    """
    # Arrange
    logger = Mock(ILogger)

    # Assert
    assert example_rule._name == "step_function_rule_name"
    assert example_rule.input_variable_names[0] == "input_variable_name"
    assert (example_rule._limits == [0, 1, 2, 5, 10]).all()
    assert isinstance(example_rule, StepFunctionRule)
    assert example_rule.validate(logger)


@pytest.mark.parametrize(
    "input_value, expected_output_value",
    [
        (0.5, 10),
        (1.5, 11),
        (2.5, 12),
        (5.5, 15),
    ],
)
def test_execute_values_between_limits(
    example_rule: StepFunctionRule, input_value: int, expected_output_value: int
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
    "input_value, expected_output_value",
    [(0, 10), (1, 11), (2, 12), (5, 15), (10, 20)],
)
def test_execute_values_at_limits(
    example_rule: StepFunctionRule, input_value: int, expected_output_value: int
):
    """
    Test the function execution with input values exactly at the interval limits.
    """
    # Arrange
    logger = Mock(ILogger)

    # Assert
    assert example_rule.execute(input_value, logger) == expected_output_value
    logger.log_warning.assert_not_called()


@pytest.mark.parametrize(
    "input_value, expected_output_value, expected_log_message",
    [(-1, 10, "value less than min"), (11, 20, "value greater than max")],
)
def test_execute_values_outside_limits(
    example_rule: StepFunctionRule,
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


def test_limits_and_responses_have_different_lengths(example_rule: StepFunctionRule):
    """
    Test the function execution when limits and responses have different lengths
    """
    # Arrange
    logger = Mock(ILogger)

    # Act
    example_rule._limits = _np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    # Assert
    assert not example_rule.validate(logger)
    logger.log_error.assert_called_with(
        "The number of limits and of responses must be equal."
    )


def test_limits_must_be_unique(example_rule: StepFunctionRule):
    """The ParserStepFunctionRule cannot sort
    limits if they are not unique. An error message should be sent."""
    # Arrange
    logger = Mock(ILogger)

    # Act
    example_rule._limits = _np.array([0, 1, 2, 5, 1])

    # Assert
    assert not example_rule.validate(logger)
    logger.log_error.assert_called_with("Limits must be unique.")
