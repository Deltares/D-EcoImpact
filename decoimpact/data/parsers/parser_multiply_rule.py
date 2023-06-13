"""
Module for ParserMultiplyRule class

Classes:
    ParserMultiplyRule
"""
from typing import Any, Dict

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import convert_table_element, get_dict_element
from decoimpact.data.entities.multiply_rule_data import MultiplyRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.validation_utils import (
    validate_all_instances_number, validate_type_date
)


class ParserMultiplyRule(IParserRuleBase):

    """Class for creating a MultiplyRuleData"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "multiply_rule"

    def parse_dict(self, dictionary: Dict[str, Any], logger: ILogger) -> IRuleData:
        """Parses the provided dictionary to a IRuleData
        Args:
            dictionary (Dict[str, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            RuleBase: Rule based on the provided data
        """
        name = get_dict_element("name", dictionary)
        input_variable_name = get_dict_element("input_variable", dictionary)
        output_variable_name = get_dict_element("output_variable", dictionary)

        multipliers = [get_dict_element("multipliers", dictionary, False)]
        date_range = []

        if not multipliers[0]:
            multipliers_table = get_dict_element("multipliers_table", dictionary)
            multipliers_dict = convert_table_element(multipliers_table)
            multipliers = get_dict_element("multipliers", multipliers_dict)
            start_date = get_dict_element("start_date", multipliers_dict)
            end_date = get_dict_element("end_date", multipliers_dict)
            if not start_date or not end_date:
                raise ValueError("Define a column for start_date and end_date!")

            validate_type_date(start_date, "start_date")
            validate_type_date(end_date, "end_date")

            date_range = list(zip(start_date, end_date))
        validate_all_instances_number(sum(multipliers, []), "Multipliers")

        return MultiplyRuleData(
            name,
            multipliers,
            input_variable_name,
            output_variable_name,
            date_range=date_range
        )