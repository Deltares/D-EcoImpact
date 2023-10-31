# This file is part of D-EcoImpact
# Copyright (C) 2022-2023  Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the GNU
# Lesser General Public License version 2.1
# A copy of the GNU General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ParserRollingStatisticsRule class

Classes:
    ParserRollingStatisticsRule
"""
from typing import Any, Dict

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.api.time_operation_type import TimeOperationType
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.entities.rolling_statistics_rule_data import (
    RollingStatisticsRuleData,
)
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase


class ParserRollingStatisticsRule(IParserRuleBase):

    """Class for creating a RollingStatisticsRuleData"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "rolling_statistics_rule"

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
        operation = get_dict_element("operation", dictionary)
        time_scale = get_dict_element("time_scale", dictionary)
        period = get_dict_element("period", dictionary)
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
        operation_parameter = None

        if not operation_value:
            message = f"Operation is not of a predefined type. Should be in: \
                      {[o.name for o in TimeOperationType]}. Received: {operation}"
            raise ValueError(message)
        if not period:
            message = f"Period is not of a predefined type. Should be  \
                      a float or integer value. Received: {period}"
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

        return RollingStatisticsRuleData(
            name,
            operation_value,
            operation_parameter,
            input_variable_name,
            output_variable_name,
            period,
            time_scale,
        )
