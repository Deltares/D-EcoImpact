# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ParserFilterExtremesRule class

Classes:
    ParserFilterExtremesRule
"""
from typing import Any, Dict, List

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.entities.filter_extremes_rule_data import FilterExtremesRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.business.entities.rules.options.options_filter_extreme_rule import (
    ExtremeTypeOptions,
)
from decoimpact.data.parsers.validation_utils import validate_type


class ParserFilterExtremesRule(IParserRuleBase):
    """Class for creating a ParserFilterExtremesRule"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "filter_extremes_rule"

    def parse_dict(self, dictionary: Dict[str, Any], logger: ILogger) -> IRuleData:
        """Parses the provided dictionary to a IRuleData
        Args:
            dictionary (Dict[str, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            RuleBase: Rule based on the provided data
        """
        name: str = get_dict_element("name", dictionary)
        input_variable_names: List[str] = [
            get_dict_element("input_variable", dictionary)
        ]
        output_variable_name: str = get_dict_element("output_variable", dictionary)
        description: str = get_dict_element("description", dictionary, False) or ""

        extreme_type_name = "extreme_type"
        extreme_type: str = get_dict_element(extreme_type_name, dictionary)
        self._validate_extreme_type(extreme_type, extreme_type_name)

        distance_name = "distance"
        distance: int = get_dict_element("distance", dictionary) or 0
        validate_type(distance, distance_name, int)

        time_scale: str = get_dict_element("time_scale", dictionary) or "D"

        mask_name = "mask"
        mask: bool = get_dict_element("mask", dictionary) or False
        validate_type(mask, mask_name, bool)

        rule_data = FilterExtremesRuleData(
            name, input_variable_names, extreme_type, distance, time_scale, mask
        )

        rule_data.output_variable = output_variable_name
        rule_data.description = description

        return rule_data

    def _validate_extreme_type(self, extreme_type: Any, name: str):
        """
        Validates if the extreme type is well formed (a string)
        and has the correct values
        """
        validate_type(extreme_type, name, str)
        if extreme_type.upper() not in dir(ExtremeTypeOptions):
            message = (
                f"""Extreme_type must be one of: [{', '.join(ExtremeTypeOptions)}]"""
            )
            raise ValueError(message)
