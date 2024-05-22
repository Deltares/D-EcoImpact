# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ParserLayerFilterRule class

Classes:
    ParserLayerFilterRule
"""
from typing import Any, Dict

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.entities.axis_filter_rule_data import AxisFilterRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase


class ParserAxisFilterRule(IParserRuleBase):
    """Class for creating a AxisFilterRuleData"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "axis_filter_rule"

    def parse_dict(self, dictionary: Dict[str, Any], logger: ILogger) -> IRuleData:
        """Parses the provided dictionary to a IRuleData
        Args:
            dictionary (Dict[str, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            RuleBase: Rule based on the provided data
        """
        name = get_dict_element("name", dictionary)
        description = get_dict_element("description", dictionary)
        input_variable_name = get_dict_element("input_variable", dictionary)
        axis_name = get_dict_element("axis_name", dictionary)
        if not isinstance(axis_name, str):
            message = (
                "Dimension name should be a string, "
                f"received a {type(axis_name)}: {axis_name}"
            )
            raise ValueError(message)

        layer_number = get_dict_element("layer_number", dictionary)
        if not isinstance(layer_number, int):
            message = (
                "Layer number should be an integer, "
                f"received a {type(layer_number)}: {layer_number}"
            )
            raise ValueError(message)
        output_variable_name = get_dict_element("output_variable", dictionary)

        rule_data = AxisFilterRuleData(
            name,
            layer_number,
            axis_name,
            input_variable_name,
        )

        rule_data.output_variable = output_variable_name
        rule_data.description = description

        return rule_data
