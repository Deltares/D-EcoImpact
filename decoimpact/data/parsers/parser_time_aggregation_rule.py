"""
Module for ParserTimeAggregationRule class

Classes:
    ParserTimeAggregationRule
"""
from typing import Any, Dict

from decoimpact.business.entities.rules.operation_type import OperationType
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.entities.time_aggregation_rule_data import TimeAggregationRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase


class ParserTimeAggregationRule(IParserRuleBase):

    """Class for creating a TimeAggregationRuleData"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "time_aggregation_rule"

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
        operation = get_dict_element("operation", dictionary)

        if not any(o.name == operation for o in OperationType):
            message = f"Operation is not of a predefined type. Should be in: \
                      {[o.name for o in OperationType]}. Received: {operation}"
            raise ValueError(message)
        output_variable_name = get_dict_element("output_variable", dictionary)

        return TimeAggregationRuleData(
            name, operation, input_variable_name, output_variable_name
        )
