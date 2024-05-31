# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ParserTimeAggregationRule class

Classes:
    ParserTimeAggregationRule
"""
from typing import Any, Dict

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.entities.time_aggregation_rule_data import TimeAggregationRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.time_operation_parsing import parse_operation_values


class ParserTimeAggregationRule(IParserRuleBase):
    """Class for creating a TimeAggregationRuleData"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "time_aggregation_rule"

    def parse_dict(self, dictionary: Dict[str, Any], logger: ILogger) -> IRuleData:
        """Parses the provided dictionary to a IRuleData
        Args:
            dictionary (Dict[str, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            RuleBase: Rule based on the provided data
        """
        # get elements
        name: str = get_dict_element("name", dictionary)
        description: str = get_dict_element("description", dictionary, False)
        input_variable_name: str = get_dict_element("input_variable", dictionary)
        operation: str = get_dict_element("operation", dictionary)
        time_scale: str = get_dict_element("time_scale", dictionary)
        output_variable_name: str = get_dict_element("output_variable", dictionary)

        operation_value, percentile_value = parse_operation_values(operation)

        rule_data = TimeAggregationRuleData(name, operation_value, input_variable_name)

        rule_data.percentile_value = percentile_value
        rule_data.time_scale = time_scale
        rule_data.output_variable = output_variable_name
        rule_data.description = description

        return rule_data
