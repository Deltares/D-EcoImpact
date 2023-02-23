"""
Tests for the ParserStepFunctionRule class
"""

from typing import Any, Dict

import pytest
from mock import Mock

from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.business.entities.rules.step_function_rule import StepFunctionRule
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.entities.step_function_data import StepFunctionRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
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

    # Act
    step_function_data = parser.parse_dict(new_dict)

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

    # Act
    with pytest.raises(AttributeError) as exc_info:
        parser.parse_dict(example_step_function_dict)

    exception_raised = exc_info.value

    # Assert
    assert exception_raised.args[0] == "Missing element " + argument_to_remove
