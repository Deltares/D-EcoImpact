"""
Tests for the ParserStepFunctionRule class
"""

import random

import pytest
from mock import Mock

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.entities.step_function_data import StepFunctionRuleData
from decoimpact.data.parsers.parser_step_function_rule import ParserStepFunctionRule


def _get_example_step_function_dict():
    return dict(
        {
            "name": "Apply chloride policy",
            "description": "this rules indicates whether the chloride policy should be applied (1.0) or not (0.0) depending on the chloride concentration.",
            "limits": [1.0, 450],
            "responses": [1.0, 0.0],
            "input_variable": "chloride_top_layer",
            "output_variable": "response_chloride_top_layer",
        }
    )


def test_parser_step_function_rule_correct_input():
    """The ParserStepFunctionRule should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Arrange
    new_dict = dict(
        {
            "name": "Test name",
            "description": "Test description",
            "limits": [0.0, 1.0, 2.0, 10.0],
            "responses": [10.0, 20.0, 30.0, 40.0],
            "input_variable": "test input variable name",
            "output_variable": "test output variable name",
        }
    )
    parser = ParserStepFunctionRule()
    logger = Mock(ILogger)

    # Act
    step_function_data = parser.parse_dict(new_dict, logger)

    # Assert
    assert isinstance(step_function_data, StepFunctionRuleData)

    assert parser.rule_type_name == "step_function_rule"
    assert step_function_data.name == "Test name"
    assert step_function_data.description == "Test description"
    assert step_function_data.limits == [0.0, 1.0, 2.0, 10.0]
    assert step_function_data.responses == [10.0, 20.0, 30.0, 40.0]
    assert step_function_data.input_variable == "test input variable name"
    assert step_function_data.output_variable == "test output variable name"


@pytest.mark.parametrize(
    "argument_to_remove",
    ["name", "responses", "limits", "input_variable", "output_variable"],
)
def test_parser_step_function_rule_missing_argument(argument_to_remove: str):
    """The ParserStepFunctionRule should give an error message
    indicating which argument is missing"""

    # Arrange
    example_step_function_dict = _get_example_step_function_dict()
    example_step_function_dict.pop(argument_to_remove)
    parser = ParserStepFunctionRule()
    logger = Mock(ILogger)

    # Act
    with pytest.raises(AttributeError) as exc_info:
        parser.parse_dict(example_step_function_dict, logger)

    exception_raised = exc_info.value

    # Assert
    assert exception_raised.args[0] == "Missing element " + argument_to_remove


def test_parser_does_not_change_ordered__limits():
    """The ParserStepFunctionRule should sort all values for
    limits in an increasing order. The respective responses
    should also be sorted accordingly."""
    # Arrange
    rule_dict = dict(
        {
            "name": "Test name",
            "description": "Test description",
            "limits": [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
            "responses": [
                0.0,
                10.0,
                20.0,
                30.0,
                40.0,
                50.0,
                60.0,
                70.0,
                80.0,
                90.0,
                100.0,
            ],
            "input_variable": "test input variable name",
            "output_variable": "test output variable name",
        }
    )
    parser = ParserStepFunctionRule()
    logger = Mock(ILogger)

    # Act
    parser.parse_dict(rule_dict, logger)

    # Assert
    logger.log_warning.assert_not_called()


def test_parser_sorts_unordered_limits():
    """The ParserStepFunctionRule should sort all values for
    limits in an increasing order. The respective responses
    should also be sorted accordingly."""
    # Arrange
    rule_dict = dict(
        {
            "name": "Test name",
            "description": "Test description",
            "limits": [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0],
            "responses": [
                0.0,
                10.0,
                20.0,
                30.0,
                40.0,
                50.0,
                60.0,
                70.0,
                80.0,
                90.0,
                100.0,
            ],
            "input_variable": "test input variable name",
            "output_variable": "test output variable name",
        }
    )
    parser = ParserStepFunctionRule()
    logger = Mock(ILogger)
    expected_log_message = "Limits were not ordered. They have been sorted increasingly, and their respective responses accordingly too."

    # Act
    original_step_function_data = parser.parse_dict(rule_dict, logger)
    temp_limits = rule_dict["limits"]
    temp_responses = rule_dict["responses"]
    temp_tuple = list(zip(temp_limits, temp_responses))
    random.shuffle(temp_tuple)
    temp_limits, temp_responses = map(list, zip(*temp_tuple))
    rule_dict["limits"] = temp_limits
    rule_dict["responses"] = temp_responses
    comparison_step_function_data = parser.parse_dict(rule_dict, logger)

    # Assert
    assert not original_step_function_data.limits == temp_limits
    assert not original_step_function_data.responses == temp_responses
    assert original_step_function_data.limits == comparison_step_function_data.limits
    assert (
        original_step_function_data.responses == comparison_step_function_data.responses
    )
    logger.log_warning.assert_called_with(expected_log_message)
