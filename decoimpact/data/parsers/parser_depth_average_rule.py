# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ParserDepthAverageRule class

Classes:
    ParserDepthAverageRule
"""
from typing import Any, Dict, List

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.entities.depth_average_rule_data import DepthAverageRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase


class ParserDepthAverageRule(IParserRuleBase):
    """Class for creating a ParserDepthAverageRule"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "depth_average_rule"

    def parse_dict(self, dictionary: Dict[str, Any], logger: ILogger) -> IRuleData:
        """Parses the provided dictionary to a IRuleData
        Args:
            dictionary (Dict[str, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            RuleBase: Rule based on the provided data
        """
        name: str = get_dict_element("name", dictionary)
        bed_level_variable = get_dict_element("bed_level_variable", dictionary)
        water_level_variable = get_dict_element("water_level_variable", dictionary)
        interfaces_variable = get_dict_element("interfaces_variable", dictionary)

        input_variable_names: List[str] = [
            get_dict_element("input_variable", dictionary),
            bed_level_variable,
            water_level_variable,
            interfaces_variable,
        ]

        output_variable_name: str = get_dict_element("output_variable", dictionary)
        description: str = get_dict_element("description", dictionary, False) or ""

        rule_data = DepthAverageRuleData(
            name,
            input_variable_names,
        )

        rule_data.output_variable = output_variable_name
        rule_data.description = description

        return rule_data
