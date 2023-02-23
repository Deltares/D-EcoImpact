"""
Module for ParserStepFunctionRule class
Classes:
    ParserStepFunctionRule
"""
from typing import Any

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.entities.step_function_data import StepFunctionRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase


class ParserStepFunctionRule(IParserRuleBase):

    """Class for creating a StepFunction"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "step_function_rule"

    def parse_dict(self, dictionary: dict[Any, Any]) -> IRuleData:
        """Parses the provided dictionary to a rule
        Args:
            dictionary (dict[Any, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            RuleBase: Rule based on the provided data
        """
        name = get_dict_element("name", dictionary)
        input_variable_name = get_dict_element("input_variable", dictionary)
        limits = get_dict_element("limits", dictionary)
        responses = get_dict_element("responses", dictionary)
        output_variable_name = get_dict_element("output_variable", dictionary)
        rule_description = get_dict_element("description", dictionary, False)

        return StepFunctionRuleData(
            name,
            limits,
            responses,
            input_variable_name,
            description=rule_description,
            output_variable=output_variable_name,
        )
