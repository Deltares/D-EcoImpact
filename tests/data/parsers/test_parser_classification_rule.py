# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for ParserClassificationRule class
"""

from typing import Any, List
import pytest
from mock import Mock

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.parser_classification_rule import ParserClassificationRule


def test_parser_classification_rule_creation_logic():
    """The ParserClassificationRule should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = ParserClassificationRule()

    # Assert

    assert isinstance(data, IParserRuleBase)
    assert data.rule_type_name == "classification_rule"


def test_parse_dict_to_rule_data_logic():
    """Test if a correct dictionary is parsed into a RuleData object"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variables": ["mesh2d_sa1", "mesh2d_waterdepth"],
            "description": "test",
            "criteria_table": [
                ["output", "mesh2d_waterdepth", "mesh2d_sa1"],
                [100, 0, 30],
                [300, 0, 0.5],
                [400, 0, "0.3:0.6"]
            ],
            "output_variable": "output",
        }
    )
    logger = Mock(ILogger)
    # Act
    data = ParserClassificationRule()
    parsed_dict = data.parse_dict(contents, logger)

    assert isinstance(parsed_dict, IRuleData)