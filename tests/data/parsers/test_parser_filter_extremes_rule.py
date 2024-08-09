# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for ParserFilterExtremesRule class
"""

from typing import Any, List
import pytest
from mock import Mock

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.parser_filter_extremes_rule import ParserFilterExtremesRule


def test_parser_filter_extremes_rule_creation_logic():
    """The ParserFilterExtremesRule should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = ParserFilterExtremesRule()

    # Assert

    assert isinstance(data, IParserRuleBase)
    assert data.rule_type_name == "filter_extremes_rule"


def test_parse_dict_to_rule_data_logic():
    """Test if a correct dictionary is parsed into a RuleData object"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variable": "input",
            "output_variable": "output",
            "distance": 1,
            "time_scale": "hour",
            "mask": True,
            "extreme_type": "peaks",
        }
    )
    logger = Mock(ILogger)
    # Act
    data = ParserFilterExtremesRule()
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
            "time_scale": "hour",
            "mask": True,
            "extreme_type": "peaks",
        }
    )
    logger = Mock(ILogger)

    # Act
    data = ParserFilterExtremesRule()

    with pytest.raises(AttributeError) as exc_info:
        data.parse_dict(contents, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "Missing element distance"
    assert exception_raised.args[0] == expected_message


@pytest.mark.parametrize(
    "extreme_type, expected_message",
    [
        ("peaks", ""),
        ("troughs", ""),
        ("test", "Extreme_type must be one of: [peaks, troughs]"),
        (
            1,
            "Extreme_type must be a string, \
                received: 1",
        ),
    ],
)
def test_validate_extreme_type(extreme_type: str, expected_message: str):
    """Test if a correct dictionary is parsed into a RuleData object"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variable": "input",
            "output_variable": "output",
            "distance": 1,
            "time_scale": "hour",
            "mask": True,
            "extreme_type": extreme_type,
        }
    )
    logger = Mock(ILogger)
    # Act
    data = ParserFilterExtremesRule()
    # Act

    if not expected_message:
        parsed_dict = data.parse_dict(contents, logger)
        assert isinstance(parsed_dict, IRuleData)
    else:
        with pytest.raises(ValueError) as exc_info:
            data.parse_dict(contents, logger=Mock(ILogger))
        exception_raised = exc_info.value

        # Assert
        assert exception_raised.args[0] == expected_message
