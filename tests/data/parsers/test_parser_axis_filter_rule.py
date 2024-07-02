# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for AxisLayerFilterRule class
"""

import pytest
from mock import Mock

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.parser_axis_filter_rule import ParserAxisFilterRule


def test_parser_axis_filter_rule_creation_logic():
    """The ParserAxisFilterRule should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = ParserAxisFilterRule()

    # Assert

    assert isinstance(data, IParserRuleBase)
    assert data.rule_type_name == "axis_filter_rule"


def test_parse_dict_to__axis_rule_data_logic():
    """Test if a correct dictionary is parsed into a RuleData object"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "description": "description",
            "input_variable": "input",
            "layer_number": 3,
            "axis_name": "axis_name",
            "output_variable": "output",
        }
    )
    logger = Mock(ILogger)

    # Act
    data = ParserAxisFilterRule()
    parsed_dict = data.parse_dict(contents, logger)

    # Assert
    assert isinstance(parsed_dict, IRuleData)


def test_parse_wrong_dict_to_axis_rule_data_logic():
    """Test if an incorrect dictionary is not parsed"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "description": "description",
            "layer_number": 3,
            "input_variable": "input",
            "output_variable": "output",
        }
    )
    logger = Mock(ILogger)

    # Act
    data = ParserAxisFilterRule()

    with pytest.raises(AttributeError) as exc_info:
        data.parse_dict(contents, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "Missing element axis_name"
    assert exception_raised.args[0] == expected_message


def test_parse_axis_name_type():
    """Test if an incorrect dictionary is not parsed"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "description": "description",
            "input_variable": "input",
            "layer_number": 3,
            "axis_name": 3,
            "output_variable": "output",
        }
    )
    logger = Mock(ILogger)

    # Act
    data = ParserAxisFilterRule()
    with pytest.raises(ValueError) as exc_info:
        data.parse_dict(contents, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "Dimension name should be a string, received a <class 'int'>: 3"
    assert exception_raised.args[0] == expected_message
