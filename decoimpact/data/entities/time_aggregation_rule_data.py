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

from typing import Optional

from decoimpact.data.api.i_time_aggregation_rule_data import ITimeAggregationRuleData
from decoimpact.data.api.time_operation_type import TimeOperationType
from decoimpact.data.entities.time_operation_rule_data import TimeOperationRuleData


class TimeAggregationRuleData(TimeOperationRuleData, ITimeAggregationRuleData):
    """Class for storing data related to time_aggregation rule"""

    def __init__(
        self,
        name: str,
        input_variable: str,
        operation: TimeOperationType,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
    ):
        super().__init__(name, operation)
        self._name = name
        self._operation = operation
        self._input_variable = input_variable
        self._start_year = start_year
        self._end_year = end_year

    # @property
    # def input_variable(self) -> str:
    #     """Name of the input variable"""
    #     return self._input_variable

    # @property
    # def start_year(self) -> Optional[int]:
    #     """Start year for aggregation"""
    #     return self._start_year

    # @property
    # def end_year(self) -> Optional[int]:
    #     """End year for aggregation"""
    #     return self._end_year
