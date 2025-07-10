# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for ParserFormulaRule class
"""

from typing import Any

import pytest
from mock import Mock

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.formula_rule_data import FormulaRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.parser_formula_rule import ParserFormulaRule


def test_parser_formula_rule_creation_logic():
    """The ParserFormulaRule should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    rule = ParserFormulaRule()

    # Assert
    assert isinstance(rule, IParserRuleBase)
    assert rule.rule_type_name == "formula_rule"


def test_parse_dict_to_rule_data_logic():
    """Test if a correct dictionary is parsed into a RuleData object"""
    # Arrange
    contents = {
        "name": "testname",
        "input_variables": ["foo", "bar"],
        "formula": "foo - bar",
        "output_variable": "test_output_name",
        "description": "test description",
    }
    logger = Mock(ILogger)

    # Act
    parser = ParserFormulaRule()
    parsed_dict = parser.parse_dict(contents, logger)

    # Assert
    assert isinstance(parsed_dict, IRuleData)
    assert isinstance(parsed_dict, FormulaRuleData)
    assert parsed_dict.name == "testname"
    assert parsed_dict.input_variable_names == ["foo", "bar"]
    assert parsed_dict.formula == "foo - bar"
    assert parsed_dict.output_variable == "test_output_name"
    assert parsed_dict.description == "test description"


def test_parse_dict_without_description():
    """Test if description is set to empty string when not passed"""
    # Arrange
    contents = {
        "name": "testname",
        "input_variables": ["foo", "bar"],
        "formula": "foo * bar",
        "output_variable": "test_output_name",
    }

    # Act
    parser = ParserFormulaRule()
    parsed_dict = parser.parse_dict(contents, logger=Mock(ILogger))

    # Assert
    assert parsed_dict.description == ""


def test_parse_wrong_dict_to_rule_data_logic():
    """Test if the formula is included or not"""
    # Arrange
    contents = {
        "name": "testname",
        "input_variables": ["foo", "bar"],
        "output_variable": "output",
    }

    # Act
    data = ParserFormulaRule()

    with pytest.raises(AttributeError) as exc_info:
        data.parse_dict(contents, logger=Mock(ILogger))

    exception_raised = exc_info.value

    # Assert
    expected_message = "Missing element formula"
    assert exception_raised.args[0] == expected_message


def test_error_if_parse_formula_not_given_by_string():
    """Test error if the formula is not a string"""
    # Arrange
    formula = 2
    contents = {
        "name": "testname",
        "input_variables": "input",
        "formula": formula,
        "output_variable": "output",
    }
    rule = ParserFormulaRule()

    # Act
    with pytest.raises(ValueError) as exc_info:
        rule.parse_dict(contents, logger=Mock(ILogger))
    exception_raised = exc_info.value

    # Assert
    expected_message = f"""Formula must be a string, \
                received: {str(formula)} (type: <class 'int'>)"""
    assert exception_raised.args[0] == expected_message
