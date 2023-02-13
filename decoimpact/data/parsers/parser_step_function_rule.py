"""
Module for ParserStepFunctionRule class
Classes:
    ParserStepFunctionRule
"""
from typing import Any, Dict

from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.business.entities.rules.step_function_rule import StepFunction
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase


class ParserStepFunctionRule(IParserRuleBase):

    """Class for creating a StepFunction"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "step_function_rule"

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
        limits = get_dict_element("limits", dictionary)
        responses = get_dict_element("responses", dictionary)

        rule = StepFunction(name, input_variable_name, limits, responses)

        rule.output_variable_name = get_dict_element("output_variable", dictionary)

        return rule