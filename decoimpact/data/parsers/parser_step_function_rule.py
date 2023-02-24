"""
Module for ParserStepFunctionRule class
Classes:
    ParserStepFunctionRule
"""
from typing import Any, List

from decoimpact.crosscutting.i_logger import ILogger
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

    def parse_dict(self, dictionary: dict[str, Any], logger: ILogger) -> IRuleData:
        """Parses the provided dictionary to a rule
        Args:
            dictionary (dict[str, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            RuleBase: Rule based on the provided data
        """
        name: str = get_dict_element("name", dictionary)
        input_variable_name: str = get_dict_element("input_variable", dictionary)
        limits: List[float] = get_dict_element("limits", dictionary)
        responses: List[float] = get_dict_element("responses", dictionary)
        output_variable_name: str = get_dict_element("output_variable", dictionary)
        rule_description: str = get_dict_element("description", dictionary, False)

        limits_are_sorted = all(a <= b for a, b in zip(limits, limits[1:]))
        if not limits_are_sorted:
            logger.log_warning(
                "Limits were not ordered. They have been sorted increasingly,"
                " and their respective responses accordingly too."
            )
            unsorted_map = list(zip(limits, responses))
            sorted_map = sorted(unsorted_map, key=lambda x: x[0])
            limits, responses = map(list, zip(*sorted_map))

        return StepFunctionRuleData(
            name,
            limits,
            responses,
            input_variable_name,
            description=rule_description,
            output_variable=output_variable_name,
        )
