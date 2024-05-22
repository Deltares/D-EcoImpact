# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for Parser FormulaRule class

Classes:
    FormulaRuleParser
"""
from typing import Any, Dict

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.entities.formula_rule_data import FormulaRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase


class ParserFormulaRule(IParserRuleBase):
    """Class for creating a FormulaRuleData"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "formula_rule"

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
        formula: str = get_dict_element("formula", dictionary, True)
        self._validate_formula(formula)
        output_variable_name = get_dict_element("output_variable", dictionary)
        description = get_dict_element("description", dictionary, False)
        if not description:
            description = ""

        rule_data = FormulaRuleData(name, input_variable_names, formula)
        rule_data.output_variable = output_variable_name
        rule_data.description = description

        return rule_data

    def _validate_formula(self, formula: str):
        """
        Validates if the formula is well formed (a string)."""
        if not isinstance(formula, str):
            message = f"""Formula must be a string, \
                received: {formula} (type: {type(formula)})"""
            raise ValueError(message)
