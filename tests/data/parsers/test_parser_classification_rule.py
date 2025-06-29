# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for ParserClassificationRule class
"""

import pytest
from mock import Mock, call

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
            """Overlap for variable varA, multiple criteria with operators < or <= are defined.\nGap for variable varA in range 8.0:inf.""",
        ),
        (
            [["output", "varB"], [1, ">0"], [2, ">=8"]],
            """Overlap for variable varB, multiple criteria with operators > or >= are defined.\nGap for variable varB in range -inf:0.0.""",
        ),
        (
            [["output", "varC"], [1, "<0"]],
            """Gap for variable varC in range 0.0:inf.""",
        ),
        (
            [["output", "varD"], [1, ">=0"]],
            """Gap for variable varD in range -inf:0.0.""",
        ),
        (
            [["output", "varE"], [1, ">0"], [2, "<10"]],
            """Overlap for variable varE in range 0.0:10.0.""",
        ),
        (
            [["output", "varF"], [1, ">0"], [2, "<0"]],
            """Gap for variable varF in number 0.0.""",
        ),
        (
            [["output", "varF2"], [1, ">0"], [2, "<=0"]],
            "",
        ),
        (
            [["output", "varF3"], [1, ">=0"], [2, "<0"]],
            "",
        ),
        (
            [["output", "varG"], [1, ">=0"], [2, "<=0"]],
            "Overlap for variable varG in number 0.0.",
        ),
        (
            [["output", "varH"], [1, "0:10"]],
            """Gap for variable varH in range -inf:0.0.\nGap for variable varH in range 10.0:inf.""",
        ),
        (
            [["output", "varH2"], [1, "0:10"], [1, "10:15"]],
            """Gap for variable varH2 in range -inf:0.0.\nOverlap for variable varH2 in number 10.0.\nGap for variable varH2 in range 15.0:inf.""",
        ),
        (
            [["output", "varI"], [1, ">0"], [2, "<0"], [3, 0]],
            "",
        ),
        (
            [["output", "varJ"], [1, "<0"], [2, "3:5"], [3, 7]],
            "Gap for variable varJ in range 0.0:3.0.\nGap for variable varJ in range 5.0:7.0.\nGap for variable varJ in range 7.0:inf.",
        ),
        (
            [["output", "varK"], [1, "0:10"], [2, "3:5"]],
            "Gap for variable varK in range -inf:0.0.\nOverlap for variable varK in range 3.0:5.0.\nGap for variable varK in range 10.0:inf.",
        ),
        (
            [["output", "varL"], [1, "0:5"], [2, "10:15"], [3, "15:20"], [4, "7:17"]],
            "Gap for variable varL in range -inf:0.0.\nGap for variable varL in range 5.0:7.0.\nOverlap for variable varL in range 10.0:15.0.\nOverlap for variable varL in range 15.0:17.0.\nGap for variable varL in range 20.0:inf.",
        ),
        (
            [
                ["output", "varM"],
                [1, "<0"],
                [2, "10:15"],
                [3, "0:10"],
                [4, 0],
                [5, ">=12"],
            ],
            "Overlap for variable varM in number 0.0.\nOverlap for variable varM in number 10.0.\nOverlap for variable varM in range 12.0:15.0.",
        ),
        (
            [["output", "varN"], [1, "0:5"], [2, 3], [3, ">=3"]],
            "Gap for variable varN in range -inf:0.0.\nOverlap for variable varN in number 3.0.\nOverlap for variable varN in range 3.0:5.0.",
        ),
        (
            [["output", "varO"], [2, "-"]],
            "",
        ),
        (
            [["output", "varO1"], [1, ">0"], [2, "-"]],
            "Overlap for variable varO1 in range 0.0:inf.",
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
            "input_variables": [
                "varA",
                "varB",
                "varC",
                "varD",
                "varE",
                "varF",
                "varF2",
                "varF3",
                "varG",
                "varH",
                "varH2",
                "varI",
                "varJ",
                "varK",
                "varL",
                "varM",
                "varN",
                "varO",
                "varO1",
            ],
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


@pytest.mark.parametrize(
    "criteria_table, calls",
    [
        (
            [
                ["output", "varA", "varB", "varC"],
                [1, "<0", "<5", "<10"],
                [2, "<0", "<5", ">=10"],
                [3, "<0", ">=5", "<10"],
                [4, "<0", ">=5", ">=10"],
                [5, ">=0", "<5", "<10"],
                [6, ">=0", "<5", ">=10"],
                [7, ">=0", ">=5", "<10"],
                [8, ">=0", ">=5", ">=10"],
            ],
            [call("")],
        ),
        (
            [
                ["output", "varA", "varB", "varC"],
                [1, "<0", "<0", "0:10"],
                [2, "<0", "<0", ">10"],
                [3, "<0", ">=0", "0:10"],
            ],
            [
                call(
                    """For conditions: (varA: <0, varB: <0). Gap for variable varC in range -inf:0.0.\nFor conditions: (varA: <0, varB: >=0). Gap for variable varC in range -inf:0.0.\nFor conditions: (varA: <0, varB: >=0). Gap for variable varC in range 10.0:inf.\nGap for variable varA in range 0.0:inf."""
                )
            ],
        ),
        (
            [
                ["output", "varA", "varB", "varC"],
                [1, "<0", "<0", "0:10"],
                [2, "<0", "<0", ">10"],
                [3, "-", "-", "-"],
            ],
            [
                call(
                    """For conditions: (varA: <0, varB: <0). Gap for variable varC in range -inf:0.0.\nFor conditions: (varA: <0). Gap for variable varB in range 0.0:inf.\nOverlap for variable varA in range -inf:0.0."""
                )
            ],
        ),
        (
            [
                ["output", "MIN_water_depth_mNAP", "MAX_flow_velocity", "MAX_chloride"],
                [1, "<0.10", "-", ">300"],  # too dry
                [2, "<0.10", "-", "< 400"],  # also too dry
                [3, ">4.0", ">3.0", "-"],  # too deep
                [4, ">4.0", "<2.0", "-"],  # also too deep
                [5, "-", "-", ">400"],  # too salty
                [6, "-", ">1.5", "-"],  # too fast flowing
                [7, "-", ">1.5", ">300"],  # also to fast flowing
                [8, "0.20:4.0", "0.0:1.5", "0:400"],  # perfect for aquatic plants
            ],
            [
                call(
                    "For conditions: (MIN_water_depth_mNAP: -, MAX_flow_velocity: -). Gap for variable MAX_chloride in range -inf:400.0.\nFor conditions: (MIN_water_depth_mNAP: -, MAX_flow_velocity: >1.5). Overlap for variable MAX_chloride in range 300.0:inf.\nFor conditions: (MIN_water_depth_mNAP: 0.20:4.0, MAX_flow_velocity: 0.0:1.5). Gap for variable MAX_chloride in range -inf:0.0.\nFor conditions: (MIN_water_depth_mNAP: 0.20:4.0, MAX_flow_velocity: 0.0:1.5). Gap for variable MAX_chloride in range 400.0:inf.\nFor conditions: (MIN_water_depth_mNAP: <0.10, MAX_flow_velocity: -). Overlap for variable MAX_chloride in range 300.0:400.0.\nFor conditions: (MIN_water_depth_mNAP: -). Overlap for variable MAX_flow_velocity in range 1.5:inf."
                ),
                call(
                    "12 warnings found concerning coverage of the parameters. Only first 6 "
                    "warnings are shown. See multiple_classification_rule_warnings.log file for all warnings."
                ),
            ],
        ),
    ],
)
def test_feedback_for_criteria_multiple_parameters(criteria_table, calls):
    """Test if a correct dictionary is parsed into a RuleData object"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variables": [
                "varA",
                "varB",
                "varC",
                "varD",
                "MIN_water_depth_mNAP",
                "MAX_flow_velocity",
                "MAX_chloride",
            ],
            "description": "test",
            "criteria_table": criteria_table,
            "output_variable": "output",
        }
    )
    logger = Mock(ILogger)
    # Act
    data = ParserClassificationRule()
    data.parse_dict(contents, logger)

    logger.log_warning.assert_has_calls(calls)


def test_feedback_for_criteria_multiple_parameters_more_10_warnings():
    """Test if a correct dictionary is parsed into a RuleData object"""
    # Arrange
    contents = dict(
        {
            "name": "testname",
            "input_variables": ["varA", "varB", "varC", "varD"],
            "description": "test",
            "criteria_table": [
                ["output", "varA", "varB", "varC", "varD"],
                [1, "<0", "<0", "0:10", "5"],
                [3, "0", ">=0", "0:10", "5"],
            ],
            "output_variable": "output",
        }
    )
    logger = Mock(ILogger)
    # Act
    data = ParserClassificationRule()
    data.parse_dict(contents, logger)

    logger.log_warning.assert_called_with(
        "11 warnings found concerning coverage of the parameters. Only first 6 "
        "warnings are shown. See multiple_classification_rule_warnings.log file "
        "for all warnings."
    )
