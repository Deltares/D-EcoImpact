"""
Module for ParserResponseRule class
Classes:
    ParserResponseRule
"""


from typing import Any, Dict

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import convert_table_element, get_dict_element
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

        # read response_table and convert it to dicts with input and output values
        response_table_list = get_dict_element("response_table", dictionary)
        response_table = convert_table_element(response_table_list)
        input_values = response_table["input"]
        output_values = response_table["output"]

        # check that response table has exactly two columns:
        if not len(response_table) == 2:
            raise ValueError(
                "ERROR: response table should have exactly 2 columns"
            )

        # validate input values to be int/float
        if not all(isinstance(m, (int, float)) for m in input_values):
            message = (
                "Input values should be a list of int or floats, "
                f"received: {input_values}"
            )
            position_error = "".join(
                [
                    f"ERROR in position {index} is type {type(m)}. "
                    for (index, m) in enumerate(input_values)
                    if not isinstance(m, (int, float))
                ]
            )
            raise ValueError(f"{position_error}{message}")

        # validate output_values to be int/float
        if not all(isinstance(m, (int, float)) for m in output_values):
            message = (
                "Output values should be a list of int or floats, "
                f"received: {output_values}"
            )
            position_error = "".join(
                [
                    f"ERROR in position {index} is type {type(m)}. "
                    for (index, m) in enumerate(output_values)
                    if not isinstance(m, (int, float))
                ]
            )
            raise ValueError(f"{position_error}{message}")

        output_variable_name = get_dict_element("output_variable", dictionary)

        return ResponseCurveRuleData(
            name,
            input_variable_name,
            input_values,
            output_values,
            output_variable_name,
            description,
        )
