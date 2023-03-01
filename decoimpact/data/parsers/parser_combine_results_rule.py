"""
Module for Parser CombineResultsRule class

Classes:
    CombineResultsRuleParser
"""
from typing import Any, Dict

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.entities.combine_results_rule_data import CombineResultsRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase


class ParserCombineResultsRule(IParserRuleBase):

    """Class for creating a CombineResultsRuleData"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "combine_results_rule"

    def parse_dict(self, dictionary: Dict[str, Any]) -> IRuleData:
        """Parses the provided dictionary to a IRuleData
        Args:
            dictionary (Dict[str, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            RuleBase: Rule based on the provided data
        """
        name = get_dict_element("name", dictionary)
        input_variable_names = get_dict_element("input_variables", dictionary)
        operation_type: str = get_dict_element("operation", dictionary)
        output_variable_name = get_dict_element("output_variable", dictionary)

        if not isinstance(operation_type, str):
            message = f"""Operation should be a string, \
                received: {operation_type}"""
            raise ValueError(message)

        return CombineResultsRuleData(
            name,
            input_variable_names,
            operation_type.upper(),
            output_variable_name,
        )
