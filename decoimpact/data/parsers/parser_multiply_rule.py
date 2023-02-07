"""
Module for ParserMultiplyRule class
Classes:
    MultiplyRuleParser
"""
from typing import Any, Dict

from decoimpact.business.entities.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.business.entities.rules.multiply_rule import MultiplyRule
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.data.dictionary_utils import get_dict_element


class ParserMultiplyRule(IParserRuleBase):

    """Class for creating a MultiplyRule"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "multiply_rule"

    def parse_dict(self, dictionary: Dict[str, Any]) -> RuleBase:
        """Parses the provided dictionary to a rule
        Args:
            dictionary (Dict[str, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            RuleBase: Rule based on the provided data
        """

        name = get_dict_element("name", dictionary)
        input_variable_name = get_dict_element("input_variable", dictionary)
        multipliers = get_dict_element("multipliers", dictionary)

        rule = MultiplyRule(name, input_variable_name, multipliers)

        rule.output_variable_name = get_dict_element("output_variable", dictionary)

        return rule
