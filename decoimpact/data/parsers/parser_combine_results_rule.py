# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the 
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for Parser CombineResultsRule class

Classes:
    CombineResultsRuleParser
"""
from typing import Any, Dict

from decoimpact.business.entities.rules.multi_array_operation_type import (
    MultiArrayOperationType,
)
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.entities.combine_results_rule_data import CombineResultsRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase


class ParserCombineResultsRule(IParserRuleBase):

    """Class for creating a CombineResultsRuleData"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "combine_results_rule"

    def parse_dict(self, dictionary: Dict[str, Any], logger: ILogger) -> IRuleData:
        """Parses the provided dictionary to an IRuleData
        Args:
            dictionary (Dict[str, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            RuleBase: Rule based on the provided data
        """
        name = get_dict_element("name", dictionary, True)
        input_variable_names = get_dict_element("input_variables", dictionary, True)
        operation_type: str = get_dict_element("operation", dictionary, True)
        self._validate_operation_type(operation_type)
        operation_type = operation_type.upper()
        output_variable_name = get_dict_element("output_variable", dictionary)
        description = get_dict_element("description", dictionary, False)
        if not description:
            description = ""

        return CombineResultsRuleData(
            name,
            input_variable_names,
            operation_type,
            output_variable_name,
            description,
        )

    def _validate_operation_type(self, operation_type: str):
        """
        Validates if the operation type is well formed (a string)
        and if it has been implemented."""
        if not isinstance(operation_type, str):
            message = f"""Operation must be a string, \
                received: {operation_type}"""
            raise ValueError(message)
        if operation_type.upper() not in dir(MultiArrayOperationType):
            possible_operations = [
                "\n" + operation_name
                for operation_name in dir(MultiArrayOperationType)
                if not operation_name.startswith("_")
            ]
            message = f"""Operation must be one of: {possible_operations}"""
            raise ValueError(message)
