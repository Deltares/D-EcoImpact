# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for TimeOperationSettings class

Classes:
    TimeOperationSettings
"""

from typing import Dict

from decoimpact.data.api.time_operation_type import TimeOperationType


class TimeOperationSettings:
    """Implementation for the time operation settings"""

    def __init__(
        self,
        time_scale_mapping: Dict[str, str],
    ):
        if len(time_scale_mapping) == 0:
            raise ValueError("The time_scale_mapping does not contain any values")

        self._time_scale_mapping = time_scale_mapping
        self._time_scale = next(i for i in time_scale_mapping.keys())
        self._operation_type = TimeOperationType.AVERAGE
        self._operation_parameter = 0.0

    @property
    def operation_type(self) -> TimeOperationType:
        """Operation type property"""
        return self._operation_type

    @operation_type.setter
    def operation_type(self, operation_type: TimeOperationType):
        self._operation_type = operation_type

    @property
    def operation_parameter(self) -> float:
        """Operation parameter property"""
        return self._operation_parameter

    @operation_parameter.setter
    def operation_parameter(self, operation_parameter: float):
        self._operation_parameter = operation_parameter

    @property
    def time_scale(self) -> str:
        """Time scale property"""
        return self._time_scale

    @time_scale.setter
    def time_scale(self, time_scale: str):

        if time_scale.lower() not in self.time_scale_mapping.keys():
            raise ValueError("The time_scale property is unsupported/invalid")

        self._time_scale = time_scale.lower()

    @property
    def time_scale_mapping(self) -> Dict[str, str]:
        """Time scale mapping property"""
        return self._time_scale_mapping