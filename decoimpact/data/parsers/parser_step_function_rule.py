# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ParserStepFunctionRule class
Classes:
    ParserStepFunctionRule
"""
from typing import Any, List

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import convert_table_element, get_dict_element
from decoimpact.data.entities.step_function_data import StepFunctionRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase


class ParserStepFunctionRule(IParserRuleBase):

    """Class for creating a StepFunction"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "step_function_rule"

    def parse_dict(self, dictionary: dict[str, Any], logger: ILogger) -> IRuleData:
        """Parses the provided dictionary to a rule
        Args:
            dictionary (dict[str, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            RuleBase: Rule based on the provided data
        """
        name: str = get_dict_element("name", dictionary)
        input_variable_name: str = get_dict_element("input_variable", dictionary)
        limit_response_table_list = get_dict_element("limit_response_table", dictionary)
        limit_response_table = convert_table_element(limit_response_table_list)
        limits = limit_response_table["limit"]
        responses = limit_response_table["response"]

        output_variable_name: str = get_dict_element("output_variable", dictionary)
        description: str = get_dict_element("description", dictionary, False)

        if not all(a < b for a, b in zip(limits, limits[1:])):
            logger.log_warning(
                "Limits were not ordered. They have been sorted increasingly,"
                " and their respective responses accordingly too."
            )
            unsorted_map = list(zip(limits, responses))
            sorted_map = sorted(unsorted_map, key=lambda x: x[0])
            limits, responses = map(list, zip(*sorted_map))

        return StepFunctionRuleData(
            name,
            limits,
            responses,
            input_variable_name,
            description,
            output_variable_name,
        )

    def _are_sorted(self, list_numbers: List[float]):
        return all(a < b for a, b in zip(list_numbers, list_numbers[1:]))
