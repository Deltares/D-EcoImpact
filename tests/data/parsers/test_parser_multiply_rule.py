"""
Tests for ParserMultiplyRule class
"""

import pytest
from mock import Mock

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.parser_multiply_rule import ParserMultiplyRule


def test_parser_multiply_rule_creation_logic():
    """The ParserMultiplyRule should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = ParserMultiplyRule()

    # Assert

    assert isinstance(data, IParserRuleBase)
    assert data.rule_type_name == "multiply_rule"


def test_parse_dict_to_rule_data_logic():
    """Test if a correct dictionary is parsed into a RuleData object"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variable": "input",
            "multipliers": [0.0, 1.0],
            "output_variable": "output",
        }
    )
    logger = Mock(ILogger)
    # Act
    data = ParserMultiplyRule()
    parsed_dict = data.parse_dict(contents, logger)

    assert isinstance(parsed_dict, IRuleData)


def test_parse_wrong_dict_to_rule_data_logic():
    """Test if an incorrect dictionary is not parsed"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variable": "input",
            "output_variable": "output",
        }
    )
    logger = Mock(ILogger)

    # Act
    data = ParserMultiplyRule()

    with pytest.raises(AttributeError) as exc_info:
        data.parse_dict(contents, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "Missing element multipliers"
    assert exception_raised.args[0] == expected_message


def test_parse_multipliers_type():
    """Test if an incorrect dictionary is not parsed"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variable": "input",
            "multipliers": ["a", "b", 2],
            "output_variable": "output",
        }
    )
    logger = Mock(ILogger)

    # Act
    data = ParserMultiplyRule()
    with pytest.raises(ValueError) as exc_info:
        data.parse_dict(contents, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = (
        "ERROR in position 0 is type <class 'str'>. "
        "ERROR in position 1 is type <class 'str'>. "
        "Multipliers should be a list of int or floats, "
        "received: ['a', 'b', 2]"
    )
    assert exception_raised.args[0] == expected_message
