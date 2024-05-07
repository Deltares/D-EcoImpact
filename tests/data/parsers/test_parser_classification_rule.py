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
                [400, 0, "0.3:0.6"],
            ],
            "output_variable": "output",
        }
    )
    logger = Mock(ILogger)
    # Act
    data = ParserClassificationRule()
    parsed_dict = data.parse_dict(contents, logger)

    assert isinstance(parsed_dict, IRuleData)


@pytest.mark.parametrize(
    "criteria_table, expected_warning_msg",
    [
        (
            [["output", "varA"], [1, "<0"], [2, "<=8"]],
            """Overlap for variable varA, multiple criteria with operators < or <= are defined\nGap for variable varA in range 8.0:inf""",
        ),
        (
            [["output", "varB"], [1, ">0"], [2, ">=8"]],
            """Overlap for variable varB, multiple criteria with operators > or >= are defined\nGap for variable varB in range -inf:0.0""",
        ),
        (
            [["output", "varC"], [1, "<0"]],
            """Gap for variable varC in range 0.0:inf""",
        ),
        (
            [["output", "varD"], [1, ">=0"]],
            """Gap for variable varD in range -inf:0.0""",
        ),
        (
            [["output", "varE"], [1, ">0"], [2, "<10"]],
            """Overlap for variable varE in range 0.0:10.0""",
        ),
        (
            [["output", "varF"], [1, ">0"], [2, "<0"]],
            """Gap for variable varF in number 0.0""",
        ),
        (
            [["output", "varF"], [1, ">0"], [2, "<=0"]],
            "",
        ),
        (
            [["output", "varG"], [1, "0:10"]],
            """Gap for variable varG in range 0.0:10.0""",
        ),
    ],
)
def test_feedback_for_criteria_with_gaps_and_overlap(
    criteria_table, expected_warning_msg
):
    """Test if a correct dictionary is parsed into a RuleData object"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variables": ["varA", "varB", "varC", "varD", "varE", "varF", "varG"],
            "description": "test",
            "criteria_table": criteria_table,
            "output_variable": "output",
        }
    )
    logger = Mock(ILogger)
    # Act
    data = ParserClassificationRule()
    data.parse_dict(contents, logger)

    logger.log_warning.assert_called_with(expected_warning_msg)
