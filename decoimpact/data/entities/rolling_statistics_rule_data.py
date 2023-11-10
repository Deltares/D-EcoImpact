# This file is part of D-EcoImpact
# Copyright (C) 2022-2023  Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the GNU
# Lesser General Public License version 2.1
# A copy of the GNU General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for RollingStatisticsRuleData class

Classes:
    RollingStatisticsRuleData

"""

from decoimpact.data.api.i_rolling_statistics_rule_data import (
    IRollingStatisticsRuleData,
)
from decoimpact.data.api.time_operation_type import TimeOperationType
from decoimpact.data.entities.rule_data import RuleData


class RollingStatisticsRuleData(IRollingStatisticsRuleData, RuleData):
    """Class for storing data related to rolling_statistic rule"""

    def __init__(
        self,
        name: str,
        operation: TimeOperationType,
        operation_parameter: float,
        input_variable: str,
        period: float,
        time_scale: str = "year",
        output_variable: str = "output",
        description: str = "",
    ):
        super().__init__(name, output_variable, description)
        self._input_variable = input_variable
        self._operation = operation
        self._operation_parameter = operation_parameter
        self._time_scale = time_scale
        self._period = period

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

    @property
    def period(self) -> float:
        """Period type"""
        return self._period
