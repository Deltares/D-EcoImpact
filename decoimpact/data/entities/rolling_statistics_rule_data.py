# This file is part of D-EcoImpact
# Copyright (C) 2022-2025  Stichting Deltares and D-EcoImpact contributors
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
from decoimpact.data.entities.time_operation_rule_data import TimeOperationRuleData


class RollingStatisticsRuleData(TimeOperationRuleData, IRollingStatisticsRuleData):
    """Class for storing data related to rolling_statistic rule"""

    def __init__(
        self,
        name: str,
        operation: TimeOperationType,
        input_variable: str,
        period: float,
    ):
        super().__init__(name, operation)
        self._input_variable = input_variable
        self._period = period

    @property
    def input_variable(self) -> str:
        """Name of the input variable"""
        return self._input_variable

    @property
    def period(self) -> float:
        """Period type"""
        return self._period
