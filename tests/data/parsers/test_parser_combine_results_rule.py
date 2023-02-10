"""
Tests for ParserMultiplyRule class
"""

import pytest

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.parser_combine_results_rule import ParserCombineResultsRule


def test_parser_combine_results_rule_creation_logic():
    """The ParserMultiplyRule should parse the provided dictionary
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
            "name": "Combined water level policy",
            "input_variable_names": ["water_level_min_policy_year","water_level_max_policy_year"],
            "operation":"Multiply"
            "output_variable": "combined_water_level_policy_year",
        }
    )

    # Act
    data = ParserCombineResultsRule()
    parsed_dict = data.parse_dict(contents)

    assert isinstance(parsed_dict, IRuleData)

