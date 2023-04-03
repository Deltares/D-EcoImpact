"""
Module for ParserResponseRule class
Classes:
    ParserResponseRule
"""


from typing import Any, Dict

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.entities.response_curve_rule_data import ResponseCurveRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase


class ParserResponseCurveRule(IParserRuleBase):

    """Class for creating a ResponseRuleData"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "response_curve_rule"

    def parse_dict(self, dictionary: Dict[str, Any], logger: ILogger) -> IRuleData:
        """Parses the provided dictionary to a IRuleData
        Args:
            dictionary (Dict[str, Any]): Dictionary holding the values
                                            for making the rule
        Returns:
            RuleBase: Rule based on the provided data
        """
        name = get_dict_element("name", dictionary)
        description = get_dict_element("description", dictionary)
        input_variable_name = get_dict_element("input_variable", dictionary)
        input_values = get_dict_element("input_values", dictionary)
        if not all(isinstance(m, (int, float)) for m in input_values):
            message = (
                f"""Input values should be a list of floats, received: {input_values}"""
            )
            raise ValueError(message)
        output_values = get_dict_element("output_values", dictionary)
        if not all(isinstance(m, (int, float)) for m in output_values):
            message = f"""Output values should be a list of floats, received: {output_values}"""
            raise ValueError(message)

        output_variable_name = get_dict_element("output_variable", dictionary)
        output_variable_name = get_dict_element("output_variable", dictionary)

        return ResponseCurveRuleData(
            name,
            input_variable_name,
            input_values,
            output_values,
            output_variable_name,
            description,
        )
