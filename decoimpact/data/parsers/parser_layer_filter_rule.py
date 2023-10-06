# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
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
from decoimpact.data.entities.layer_filter_rule_data import LayerFilterRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase


class ParserLayerFilterRule(IParserRuleBase):

    """Class for creating a LayerFilterRuleData"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "layer_filter_rule"

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
        layer_number = get_dict_element("layer_number", dictionary)
        if not isinstance(layer_number, int):
            message = (
                "Layer number should be an integer, "
                f"received a {type(layer_number)}: {layer_number}"
            )
            raise ValueError(message)
        output_variable_name = get_dict_element("output_variable", dictionary)

        return LayerFilterRuleData(
            name, layer_number, input_variable_name, output_variable_name, description
        )
