"""
Tests for the ParserStepFunctionRule class
"""

from typing import Any, Dict

import pytest
from mock import Mock

from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.business.entities.rules.step_function_rule import StepFunction
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.parser_step_function_rule import ParserStepFunctionRule


@pytest.fixture
def example_step_function_dict():
    return dict(
        {
            "name": "Apply chloride policy",
            "description": "this rules indicates whether the chloride policy should be applied (1) or not (0) depending on the chloride concentration.",
            "limits": [1.0, 450],
            "responses": [1.0, 0.0],
            "input_variable": "chloride_top_layer",
            "output_variable": "response_chloride_top_layer",
        }
    )


def test_parser_step_function_rule_correct_input():
    """The ParserStepFunctionRule should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    parser = ParserStepFunctionRule()
    data = dict(
        {
            "name": "Apply chloride policy",
            "description": "this rules indicates whether the chloride policy should be applied (1) or not (0) depending on the chloride concentration.",
            "limits": [1.0, 450],
            "responses": [1.0, 0.0],
            "input_variable": "chloride_top_layer",
            "output_variable": "response_chloride_top_layer",
        }
    )
    parsed_dict = parser.parse_dict(data)

    # Assert
    assert isinstance(parsed_dict, IRuleData)
