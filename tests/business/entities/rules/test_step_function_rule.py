"""
Tests for Step Function Rule class
"""


import pytest
from mock import Mock

from decoimpact.business.entities.rules.step_function_rule import StepFunction
from decoimpact.crosscutting.i_logger import ILogger


@pytest.fixture
def example_rule():
    return StepFunction(
        "step_function_rule_name",
        "input_variable_name",
        [0, 1, 2, 5, 10],
        [10, 11, 12, 15, 20],
    )


def test_create_step_function(example_rule):
    """
    Test creating a new Step Fuction rule
    """

    assert example_rule._name == "step_function_rule_name"
    assert example_rule.input_variable_names == "input_variable_name"
    assert example_rule._intervals_limits == [0, 1, 2, 5, 10]
    assert example_rule._interval_values == [10, 11, 12, 15, 20]
    assert isinstance(example_rule, StepFunction)


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
    example_rule: StepFunction, input_value: int, expected_output_value: int
):
    """
    Test the function execution with input values between the interval limits.
    """
    logger = Mock(ILogger)

    assert example_rule.execute(input_value, logger) == expected_output_value
    logger.log_warning.assert_not_called()


@pytest.mark.parametrize(
    "input_value, expected_output_value",
    [(0, 10), (1, 11), (2, 12), (5, 15), (10, 20)],
)
def test_execute_values_at_limits(
    example_rule: StepFunction, input_value: int, expected_output_value: int
):
    """
    Test the function execution with input values exactly at the interval limits.
    """
    logger = Mock(ILogger)

    assert example_rule.execute(input_value, logger) == expected_output_value
    logger.log_warning.assert_not_called()


@pytest.mark.parametrize(
    "input_value, expected_output_value, expected_log_message",
    [(-1, 10, "value less than min"), (11, 20, "value greater than max")],
)
def test_execute_values_outside_limits(
    example_rule: StepFunction,
    input_value: int,
    expected_output_value: int,
    expected_log_message: str,
):
    """
    Test the function execution with input values outside the interval limits.
    """
    logger = Mock(ILogger)

    assert example_rule.execute(input_value, logger) == expected_output_value
    logger.log_warning.assert_called_with(expected_log_message)