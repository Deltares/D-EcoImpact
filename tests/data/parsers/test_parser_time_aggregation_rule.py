# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the 
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for ParserTimeAggregationRule class
"""

import pytest
from mock import Mock

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.api.time_operation_type import TimeOperationType
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.parser_time_aggregation_rule import (
    ParserTimeAggregationRule,
)


def test_parser_time_aggregation_rule_creation_logic():
    """The ParserTimeAggregationRule should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = ParserTimeAggregationRule()

    # Assert

    assert isinstance(data, IParserRuleBase)
    assert data.rule_type_name == "time_aggregation_rule"


def test_parse_dict_to_rule_data_logic():
    """Test if a correct dictionary is parsed into a RuleData object"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variable": "input",
            "operation": "MIN",
            "output_variable": "output",
            "time_scale": "year",
        }
    )
    logger = Mock(ILogger)

    # Act
    data = ParserTimeAggregationRule()
    parsed_dict = data.parse_dict(contents, logger)

    # Assert
    assert isinstance(parsed_dict, IRuleData)


def test_parse_wrong_dict_to_rule_data_logic():
    """Test if an incorrect dictionary is not parsed"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variable": "input",
            "output_variable": "output",
            "time_scale": "year",
        }
    )
    logger = Mock(ILogger)

    # Act
    data = ParserTimeAggregationRule()

    with pytest.raises(AttributeError) as exc_info:
        data.parse_dict(contents, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "Missing element operation"
    assert exception_raised.args[0] == expected_message


def test_parse_operation_type():
    """Test if an incorrect dictionary is not parsed"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variable": "input",
            "operation": "Minimum",
            "output_variable": "output",
            "time_scale": "year",
        }
    )
    logger = Mock(ILogger)

    # Act
    data = ParserTimeAggregationRule()
    with pytest.raises(ValueError) as exc_info:
        data.parse_dict(contents, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = f"Operation is not of a predefined type. Should be in: \
                      {[o.name for o in TimeOperationType]}. Received: Minimum"
    assert exception_raised.args[0] == expected_message
