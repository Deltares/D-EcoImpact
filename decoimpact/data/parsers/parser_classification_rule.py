# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ParserClassificationRule class

Classes:
    ParserClassificationRule
"""
from typing import Any, Dict

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import convert_table_element, get_dict_element
from decoimpact.data.entities.classification_rule_data import ClassificationRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.validation_utils import validate_table_with_input


class ParserClassificationRule(IParserRuleBase):

    """Class for creating a ClassificationRuleData"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "classification_rule"

    def parse_dict(self, dictionary: Dict[str, Any], logger: ILogger) -> IRuleData:
        """Parses the provided dictionary to a IRuleData
        Args:
            dictionary (Dict[str, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            RuleBase: Rule based on the provided data
        """
        name = get_dict_element("name", dictionary)
        input_variable_names = get_dict_element("input_variables", dictionary)
        criteria_table_list = get_dict_element("criteria_table", dictionary)
        criteria_table = convert_table_element(criteria_table_list)

        validate_table_with_input(criteria_table, input_variable_names)

        output_variable_name = get_dict_element("output_variable", dictionary)
        description = get_dict_element("description", dictionary)

        return ClassificationRuleData(
            name,
            input_variable_names,
            criteria_table,
            output_variable_name,
            description,
        )
