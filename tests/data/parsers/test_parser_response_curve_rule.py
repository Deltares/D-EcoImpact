"""
Tests for ParserResponseCurveRule class
"""

import pytest
from mock import Mock

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.parser_response_curve_rule import ParserResponseCurveRule


def _get_example_response_curve_rule_dict():
    return dict(
        {
            "name": "test_name",
            "description": "description",
            "input_variable": "input",
            "input_values": [1, 2, 3],
            "output_values": [3, 2, 0],
            "output_variable": "output",
        }
    )


def test_parser_response_curve_rule_creation_logic():
    """The ParserLayerFilterRule should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = ParserResponseCurveRule()

    # Assert

    assert isinstance(data, IParserRuleBase)
    assert data.rule_type_name == "response_curve_rule"


def test_parse_dict_to_rule_data_logic():
    """Test if a correct dictionary is parsed into a RuleData object"""
    # Arrange
    contents = _get_example_response_curve_rule_dict()
    logger = Mock(ILogger)

    # Act
    data = ParserResponseCurveRule()
    parsed_dict = data.parse_dict(contents, logger)

    # Assert
    assert isinstance(parsed_dict, IRuleData)


@pytest.mark.parametrize(
    "argument_to_remove",
    [
        "name",
        "input_values",
        "output_values",
        "input_variable",
        "output_variable",
        "description",
    ],
)
def test_parser_response_curve_rule_missing_argument(argument_to_remove: str):
    """If an argument is missing, the ParserResponseCurveRule
    should give an error message indicating which one"""

    # Arrange
    contents = _get_example_response_curve_rule_dict()
    contents.pop(argument_to_remove)

    parser = ParserResponseCurveRule()
    logger = Mock(ILogger)

    # Act
    with pytest.raises(AttributeError) as exc_info:
        parser.parse_dict(contents, logger)

    exception_raised = exc_info.value

    # Assert
    assert exception_raised.args[0] == "Missing element " + argument_to_remove


def test_parse_input_values_type():
    """Test if dictionary is not parsed in case of input_values are invalid"""
    # Arrange
    contents = dict(
        {
            "name": "test_name",
            "description": "description",
            "input_variable": "input",
            "input_values": ["a", "b", 2],
            "output_values": [3, 2, 0],
            "output_variable": "output",
        }
    )
    logger = Mock(ILogger)

    # Act
    data = ParserResponseCurveRule()
    with pytest.raises(ValueError) as exc_info:
        data.parse_dict(contents, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "Input values should be a list of floats, \
                          received: ['a', 'b', 2]"
    assert exception_raised.args[0] == expected_message


def test_parse_output_values_type():
    """Test if dictionary is not parsed in case of output_values are invalid"""
    # Arrange
    contents = dict(
        {
            "name": "test_name",
            "description": "description",
            "input_variable": "input",
            "input_values": [1, 2, 3],
            "output_values": ["a", "b", 2],
            "output_variable": "output",
        }
    )
    logger = Mock(ILogger)

    # Act
    data = ParserResponseCurveRule()
    with pytest.raises(ValueError) as exc_info:
        data.parse_dict(contents, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "Output values should be a list of floats, \
                          received: ['a', 'b', 2]"
    assert exception_raised.args[0] == expected_message
