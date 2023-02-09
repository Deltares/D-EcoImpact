"""
Module for ParserMultiplyRule class

Classes:
    MultiplyRuleParser
"""
from typing import Any, Dict

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.entities.multiply_rule_data import MultiplyRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase


class ParserMultiplyRule(IParserRuleBase):

    """Class for creating a MultiplyRuleData"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "multiply_rule"

    def parse_dict(self, dictionary: Dict[str, Any]) -> IRuleData:
        """Parses the provided dictionary to a IRuleData
        Args:
            dictionary (Dict[str, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            RuleBase: Rule based on the provided data
        """
        name = get_dict_element("name", dictionary)
        input_variable_name = get_dict_element("input_variable", dictionary)
        multipliers = get_dict_element("multipliers", dictionary)
        output_variable_name = get_dict_element("output_variable", dictionary)

        return MultiplyRuleData(
                                name,
                                multipliers,
                                input_variable_name,
                                output_variable_name)
