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
        self._validate_operation_type(operation_type)
        operation_type = operation_type.upper()
        output_variable_name = get_dict_element("output_variable", dictionary)
        description = get_dict_element("description", dictionary, False)
        if not description:
            description = ""

        return FormulaRuleData(
            name,
            input_variable_names,
            formula,
            output_variable_name,
            description,
        )

    def _validate_formula(self, formula: str):
        """
        Validates if the operation type is well formed (a string)."""
        if not isinstance(formula, str):
            message = f"""Formula must be a string, \
                received: {formula}"""
            raise ValueError(message)
