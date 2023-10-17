# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for TimeAggregationRuleData class

Classes:
    TimeAggregationRuleData

"""

from decoimpact.data.api.i_time_aggregation_rule_data import ITimeAggregationRuleData
from decoimpact.data.api.time_operation_type import TimeOperationType
from decoimpact.data.entities.rule_data import RuleData


class TimeAggregationRuleData(ITimeAggregationRuleData, RuleData):
    """Class for storing data related to time_aggregation rule"""

    def __init__(
        self,
        name: str,
        operation: TimeOperationType,
        operation_parameter: float,
        input_variable: str,
        time_scale: str = "year",
        output_variable: str = "output",
        description: str = "",
    ):
        super().__init__(name, output_variable, description)
        self._input_variable = input_variable
        self._operation = operation
        self._operation_parameter = operation_parameter
        self._time_scale = time_scale

    @property
    def input_variable(self) -> str:
        """Name of the input variable"""
        return self._input_variable

    @property
    def operation(self) -> TimeOperationType:
        """Operation type"""
        return self._operation

    @property
    def operation_parameter(self) -> float:
        """Operation parameter"""
        return self._operation_parameter

    @property
    def time_scale(self) -> str:
        """Time scale type"""
        return self._time_scale
