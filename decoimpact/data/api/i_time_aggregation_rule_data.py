# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ITimeAggregationRuleData interface

Interfaces:
    ITimeAggregationRuleData

"""


from abc import ABC, abstractmethod

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.api.time_operation_type import TimeOperationType


class ITimeAggregationRuleData(IRuleData, ABC):
    """Data for a TimeAggregationRule"""

    @property
    @abstractmethod
    def input_variable(self) -> str:
        """Name of the input variable"""

    @property
    @abstractmethod
    def operation(self) -> TimeOperationType:
        """Operation type"""

    @property
    @abstractmethod
    def percentile_value(self) -> float:
        """Operation parameter"""

    @property
    @abstractmethod
    def time_scale(self) -> str:
        """Time scale"""
