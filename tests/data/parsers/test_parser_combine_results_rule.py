"""
Tests for ParserCombinResultsRule class
"""

from typing import Any

import pytest
from mock import Mock

from decoimpact.business.entities.rules.multi_array_operation_type import (
    MultiArrayOperationType,
)
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.combine_results_rule_data import CombineResultsRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.parser_combine_results_rule import ParserCombineResultsRule


def test_parser_combine_results_rule_creation_logic():
    """The ParserCombinResultsRule should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    rule = ParserCombineResultsRule()

    # Assert
    assert isinstance(rule, IParserRuleBase)
    assert rule.rule_type_name == "combine_results_rule"


def test_parse_dict_to_rule_data_logic():
    """Test if a correct dictionary is parsed into a RuleData object"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variables": ["foo", "bar"],
            "operation": "Multiply",
            "output_variable": "test_output_name",
            "description": "test description",
        }
    )
    logger = Mock(ILogger)

    # Act
    parser = ParserCombineResultsRule()
    parsed_dict = parser.parse_dict(contents, logger)

    # Assert
    assert isinstance(parsed_dict, IRuleData)
    assert isinstance(parsed_dict, CombineResultsRuleData)
    assert parsed_dict.name == "testname"
    assert parsed_dict.input_variable_names == ["foo", "bar"]
    assert parsed_dict.operation_type == "MULTIPLY"
    assert parsed_dict.output_variable == "test_output_name"
    assert parsed_dict.description == "test description"


def test_parse_dict_without_description():
    """Test if description is set to empty string when not passed"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variables": ["foo", "bar"],
            "operation": "Multiply",
            "output_variable": "test_output_name",
        }
    )

    # Act
    parser = ParserCombineResultsRule()
    parsed_dict = parser.parse_dict(contents, logger=Mock(ILogger))

    # Assert
    assert parsed_dict.description == ""


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
        data.parse_dict(contents, logger=Mock(ILogger))

    exception_raised = exc_info.value

    # Assert
    expected_message = "Missing element operation"
    assert exception_raised.args[0] == expected_message


@pytest.mark.parametrize(
    "invalid_operation",
    [1, [2, 3, 4], (5, 5, 7, 9), {"key": "MULTIPLYI"}, lambda a: a + 10],
)
def test_error_if_parse_operation_type_not_given_by_string(invalid_operation: Any):
    """Test error if the operation is not a number"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variables": "input",
            "operation": invalid_operation,
            "output_variable": "output",
        }
    )
    rule = ParserCombineResultsRule()

    # Act
    with pytest.raises(ValueError) as exc_info:
        rule.parse_dict(contents, logger=Mock(ILogger))
    exception_raised = exc_info.value

    # Assert
    expected_message = f"""Operation must be a string, \
                received: {str(invalid_operation)}"""
    assert exception_raised.args[0] == expected_message


def test_error_if_parse_unknown_operation_type():
    """Test error if the operation type is unknown"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variables": "input",
            "operation": "unkown",
            "output_variable": "output",
        }
    )
    possible_operations = [
        "\n" + operation_name
        for operation_name in dir(MultiArrayOperationType)
        if not operation_name.startswith("_")
    ]
    expected_message = f"Operation must be one of: {possible_operations}"
    rule = ParserCombineResultsRule()

    # Act
    with pytest.raises(ValueError) as exc_info:
        rule.parse_dict(contents, logger=Mock(ILogger))
    exception_raised = exc_info.value

    # Assert
    assert exception_raised.args[0] == expected_message
