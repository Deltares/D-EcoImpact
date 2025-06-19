# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
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
from decoimpact.data.entities.time_operation_rule_data import TimeOperationRuleData


class TimeAggregationRuleData(TimeOperationRuleData, ITimeAggregationRuleData):
    """Class for storing data related to time_aggregation rule"""

    def __init__(self, name: str, operation: TimeOperationType, input_variable: str):
        super().__init__(name, operation)
        self._input_variable = input_variable

    @property
    def input_variable(self) -> str:
        """Name of the input variable"""
        return self._input_variable
