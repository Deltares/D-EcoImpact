"""
Module for ParserLayerFilterRule class
Classes:
    ParserLayerFilterRule
"""
from typing import Any, Dict

from decoimpact.business.entities.rules.layer_filter_rule import LayerFilterRule
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase


class ParserLayerFilterRule(IParserRuleBase):

    """Class for creating a ParserLayerFilterRule"""

    @property
    def rule_type_name(self) -> str:
        return "layer_filter_rule"

    def parse_dict(self, dictionary: Dict[str, Any]) -> RuleBase:
        """Parses the provided dictionary to a rule
        Args:
            dictionary (Dict[str, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            RuleBase: Rule based on the provided information
        """

        name = get_dict_element("name", dictionary)
        input_variable_name = get_dict_element("input_variable", dictionary)
        layer_number = get_dict_element("layer_number", dictionary)

        rule = LayerFilterRule(name, input_variable_name, layer_number)
        rule.output_variable_name = get_dict_element("output_variable", dictionary)
        return rule
