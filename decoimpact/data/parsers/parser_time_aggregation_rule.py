# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ParserTimeAggregationRule class

Classes:
    ParserTimeAggregationRule
"""
from typing import Any, Dict

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.api.time_operation_type import TimeOperationType
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.entities.time_aggregation_rule_data import TimeAggregationRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase


class ParserTimeAggregationRule(IParserRuleBase):
    """Class for creating a TimeAggregationRuleData"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "time_aggregation_rule"

    def parse_dict(self, dictionary: Dict[str, Any], logger: ILogger) -> IRuleData:
        """Parses the provided dictionary to a IRuleData
        Args:
            dictionary (Dict[str, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            RuleBase: Rule based on the provided data
        """
        # get elements
        name = get_dict_element("name", dictionary)
        description: str = get_dict_element("description", dictionary, False)
        input_variable_name = get_dict_element("input_variable", dictionary)
        operation = get_dict_element("operation", dictionary)
        time_scale = get_dict_element("time_scale", dictionary)
        operation_parameter = None

        # if operation contains percentile,
        # extract percentile value as operation_parameter from operation:
        if str(operation)[:10] == "PERCENTILE":
            try:
                operation_parameter = float(str(operation)[11:-1])
            except ValueError as exc:
                message = (
                    "Operation percentile is missing valid value like 'percentile(10)'"
                )
                raise ValueError(message) from exc
            operation = "PERCENTILE"

        # validate operation
        match_operation = [o for o in TimeOperationType if o.name == operation]
        operation_value = next(iter(match_operation), None)

        # validate operation_value (percentile(n); n = operation_value)
        if not operation_value:
            message = f"Operation is not of a predefined type. Should be in: \
                      {[o.name for o in TimeOperationType]}. Received: {operation}"
            raise ValueError(message)

        # test if operation_parameter is within expected limits:
        if operation_value == TimeOperationType.PERCENTILE:
            if (
                operation_parameter is None
                or operation_parameter < 0
                or operation_parameter > 100
            ):
                message = "Operation percentile should be a number between 0 and 100."
                raise ValueError(message)

        output_variable_name = get_dict_element("output_variable", dictionary)

        rule_data = TimeAggregationRuleData(
            name, operation_value, operation_parameter, input_variable_name, time_scale
        )

        rule_data.output_variable = output_variable_name
        rule_data.description = description

        return rule_data
