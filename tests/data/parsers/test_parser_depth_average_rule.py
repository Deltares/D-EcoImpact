# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for ParserDepthAverageRule class
"""

from typing import Any, List

import pytest
from mock import Mock

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.parser_depth_average_rule import ParserDepthAverageRule


def test_parser_depth_average_rule_creation_logic():
    """The ParserDepthAverageRule should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = ParserDepthAverageRule()

    # Assert

    assert isinstance(data, IParserRuleBase)
    assert data.rule_type_name == "depth_average_rule"


def test_parse_dict_to_rule_data_logic():
    """Test if a correct dictionary is parsed into a RuleData object"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variable": "input",
            "bed_level_variable": "bedlevel",
            "water_level_variable": "waterlevel",
            "interfaces_variable": "interfaces",
            "output_variable": "output",
        }
    )
    logger = Mock(ILogger)
    # Act
    data = ParserDepthAverageRule()
    parsed_dict = data.parse_dict(contents, logger)

    assert isinstance(parsed_dict, IRuleData)


def test_parse_wrong_dict_to_rule_data_logic():
    """Test if an incorrect dictionary is not parsed"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "output_variable": "output",
            "bed_level_variable": "bedlevel",
            "water_level_variable": "waterlevel",
            "interfaces_variable": "interfaces_z",
        }
    )
    logger = Mock(ILogger)

    # Act
    data = ParserDepthAverageRule()

    with pytest.raises(AttributeError) as exc_info:
        data.parse_dict(contents, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "Missing element input_variable"
    assert exception_raised.args[0] == expected_message
