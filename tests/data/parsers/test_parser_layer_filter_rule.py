"""
Tests for ParserLayerFilterRule class
"""

import pytest
from mock import Mock

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.parser_layer_filter_rule import ParserLayerFilterRule


def test_parser_layer_filter_rule_creation_logic():
    """The ParserLayerFilterRule should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = ParserLayerFilterRule()

    # Assert

    assert isinstance(data, IParserRuleBase)
    assert data.rule_type_name == "layer_filter_rule"


def test_parse_dict_to_rule_data_logic():
    """Test if a correct dictionary is parsed into a RuleData object"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "description": "description",
            "input_variable": "input",
            "layer_number": 3,
            "output_variable": "output",
        }
    )
    logger = Mock(ILogger)

    # Act
    data = ParserLayerFilterRule()
    parsed_dict = data.parse_dict(contents, logger)

    # Assert
    assert isinstance(parsed_dict, IRuleData)


def test_parse_wrong_dict_to_rule_data_logic():
    """Test if an incorrect dictionary is not parsed"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "description": "description",
            "input_variable": "input",
            "output_variable": "output",
        }
    )
    logger = Mock(ILogger)

    # Act
    data = ParserLayerFilterRule()

    with pytest.raises(AttributeError) as exc_info:
        data.parse_dict(contents, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "Missing element layer_number"
    assert exception_raised.args[0] == expected_message


def test_parse_layer_number_type():
    """Test if an incorrect dictionary is not parsed"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "description": "description",
            "input_variable": "input",
            "layer_number": "3",
            "output_variable": "output",
        }
    )
    logger = Mock(ILogger)

    # Act
    data = ParserLayerFilterRule()
    with pytest.raises(ValueError) as exc_info:
        data.parse_dict(contents, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "Layer number should be an integer, \
                received: 3"
    assert exception_raised.args[0] == expected_message
