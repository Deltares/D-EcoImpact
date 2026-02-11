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
        operation: TimeOperationType,
        input_variable: str,
        multi_year_start: Optional[int] = None,
        multi_year_end: Optional[int] = None,
    ):
        # pylint: disable=too-many-arguments
        # pylint: disable=too-many-positional-arguments
        super().__init__(name, operation)
        self._input_variable = input_variable
        self._multi_year_start = multi_year_start
        self._multi_year_end = multi_year_end

    @property
    def input_variable(self) -> str:
        """Name of the input variable"""
        return self._input_variable

    @property
    def multi_year_start(self) -> Optional[int]:
        """Start year for aggregation"""
        return self._multi_year_start

    @multi_year_start.setter
    def multi_year_start(self, value: Optional[int]) -> None:
        # optional validation here
        self._multi_year_start = value

    @property
    def multi_year_end(self) -> Optional[int]:
        """End year for aggregation"""
        return self._multi_year_end

    @multi_year_end.setter
    def multi_year_end(self, value: Optional[int]) -> None:
        # optional validation here
        self._multi_year_end = value
