"""
Tests for ParserCombinResultsRule class
"""

import pytest

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.parser_combine_results_rule import ParserCombineResultsRule


def test_parser_combine_results_rule_creation_logic():
    """The ParserCombinResultsRule should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = ParserCombineResultsRule()

    # Assert

    assert isinstance(data, IParserRuleBase)
    assert data.rule_type_name == "combine_results_rule"


def test_parse_dict_to_rule_data_logic():
    """Test if a correct dictionary is parsed into a RuleData object"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variables": ["foo", "bar"],
            "operation": "Multiply",
            "output_variable": "output",
        }
    )

    # Act
    data = ParserCombineResultsRule()
    parsed_dict = data.parse_dict(contents)

    assert isinstance(parsed_dict, IRuleData)


def test_parse_wrong_dict_to_rule_data_logic():
    """Test if the operation type is included or not"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variables": ["foo", "bar"],
            "output_variable": "output",
        }
    )

    # Act
    data = ParserCombineResultsRule()

    with pytest.raises(AttributeError) as exc_info:
        data.parse_dict(contents)

    exception_raised = exc_info.value

    # Assert
    expected_message = "Missing element operation"
    assert exception_raised.args[0] == expected_message


def test_parse_operation_type():
    """Test if the operation type is a str, but not a number"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variables": "input",
            "operation": 2,
            "output_variable": "output",
        }
    )

    # Act
    data = ParserCombineResultsRule()
    with pytest.raises(ValueError) as exc_info:
        data.parse_dict(contents)

    exception_raised = exc_info.value

    # Assert
    expected_message = """Operation should be a string, \
                received: 2"""
    assert exception_raised.args[0] == expected_message