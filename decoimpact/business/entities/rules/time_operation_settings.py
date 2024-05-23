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

from decoimpact.crosscutting.i_logger import ILogger
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
        self._percentile_value = 0.0

    @property
    def operation_type(self) -> TimeOperationType:
        """Operation type property"""
        return self._operation_type

    @operation_type.setter
    def operation_type(self, operation_type: TimeOperationType):
        self._operation_type = operation_type

    @property
    def percentile_value(self) -> float:
        """Operation parameter property"""
        return self._percentile_value

    @percentile_value.setter
    def percentile_value(self, percentile_value: float):
        self._percentile_value = percentile_value

    @property
    def time_scale(self) -> str:
        """Time scale property"""
        return self._time_scale

    @time_scale.setter
    def time_scale(self, time_scale: str):
        self._time_scale = time_scale.lower()

    @property
    def time_scale_mapping(self) -> Dict[str, str]:
        """Time scale mapping property"""
        return self._time_scale_mapping

    def validate(self, rule_name: str, logger: ILogger) -> bool:
        """Validates if the rule is valid

        Returns:
            bool: wether the rule is valid
        """
        valid = True
        allowed_time_scales = self.time_scale_mapping.keys()

        if self.time_scale not in allowed_time_scales:
            options = ",".join(allowed_time_scales)
            logger.log_error(
                f"The provided time scale '{self.time_scale}' "
                f"of rule '{rule_name}' is not supported.\n"
                f"Please select one of the following types: "
                f"{options}"
            )
            valid = False

        return valid
