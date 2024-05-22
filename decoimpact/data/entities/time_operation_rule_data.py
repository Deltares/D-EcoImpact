# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for TimeOperationRuleData class

Classes:
    TimeOperationRuleData

"""

from decoimpact.data.api.time_operation_type import TimeOperationType
from decoimpact.data.entities.rule_data import RuleData


class TimeOperationRuleData(RuleData):
    """Base class for rule data related to time operations"""

    def __init__(
        self,
        name: str,
        operation: TimeOperationType,
        operation_parameter: float,
        time_scale: str = "year",
    ):
        super().__init__(name)
        self._operation = operation
        self._operation_parameter = operation_parameter
        self._time_scale = time_scale

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
