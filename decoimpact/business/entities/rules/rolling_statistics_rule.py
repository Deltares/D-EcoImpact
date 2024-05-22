# This file is part of D-EcoImpact
# Copyright (C) 2022-2023  Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the GNU
# Lesser General Public License version 2.1
# A copy of the GNU General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for RollingStatisticsRule class

Classes:
    RollingStatisticsRule
"""

import copy as _cp
import datetime as _dt

# from itertools import groupby
from os import name
from typing import List

import numpy as _np
import xarray as _xr

from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.business.entities.rules.time_operation_settings import (
    TimeOperationSettings,
)
from decoimpact.business.utils.data_array_utils import get_time_dimension_name
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.time_operation_type import TimeOperationType
from decoimpact.data.dictionary_utils import get_dict_element


class RollingStatisticsRule(RuleBase, IArrayBasedRule):
    """Implementation for the rolling statistics rule"""

    def __init__(
        self,
        name: str,
        input_variable_names: List[str],
        operation_type: TimeOperationType,
    ):
        super().__init__(name, input_variable_names)
        self._settings = TimeOperationSettings({"hour": "H", "day": "D"})
        self._settings.operation_parameter = 0
        self._settings.operation_type = operation_type
        self._settings.time_scale = "day"
        self._period = 1

    @property
    def settings(self):
        """Time operation settings"""
        return self._settings

    @property
    def period(self) -> float:
        """Operation type property"""
        return self._period

    @period.setter
    def period(self, period: float):
        self._period = period

    def validate(self, logger: ILogger) -> bool:
        """Validates if the rule is valid

        Returns:
            bool: wether the rule is valid
        """

        return self.settings.validate(self.name, logger)

    def execute(self, value_array: _xr.DataArray, logger: ILogger) -> _xr.DataArray:
        """Calculating the rolling statistics for a given period

        Args:
            value_array (DataArray): value to aggregate

        Returns:
            DataArray: Aggregated values
        """

        time_scale = get_dict_element(
            self.settings.time_scale, self.settings.time_scale_mapping
        )

        time_dim_name = get_time_dimension_name(value_array, logger)

        result = self._perform_operation(
            value_array,
            time_dim_name,
            time_scale,
            logger,
        )
        return result

    def _perform_operation(
        self,
        values: _xr.DataArray,
        time_dim_name: str,
        time_scale: str,
        logger: ILogger,
    ) -> _xr.DataArray:
        """Returns the values based on the operation type


        Args:
            values (_xr.DataArray): values
            time_dim_name (str): time dimension name
            dim_name (str): dimension name
            logger (ILogger): logger

        Raises:
            NotImplementedError: If operation type is not supported

        Returns:
            DataArray: Values of operation type
        """

        result_array = _cp.deepcopy(values)
        result_array = result_array.where(False, _np.nan)

        if time_scale == "H":
            operation_time_delta = _dt.timedelta(hours=self._period)
        elif time_scale == "D":
            operation_time_delta = _dt.timedelta(days=self._period)
        else:
            logger.log_error(f"Invalid time scale provided : '{time_scale}'.")

        time_delta_ms = _np.array([operation_time_delta], dtype="timedelta64[ms]")[0]
        last_timestamp = values.time.isel(time=-1).values
        for time_step in values.time.values:  # Interested in vectorizing this loop
            if last_timestamp - time_step < time_delta_ms:
                break

            data = values.sel(time=slice(time_step, time_step + time_delta_ms))
            last_timestamp_data = data.time.isel(time=-1).values
            result = self._apply_operation(data, time_dim_name)

            result_array.loc[{"time": last_timestamp_data}] = result

        return _xr.DataArray(result_array)

    def _apply_operation(
        self, data: _xr.DataArray, time_dim_name: str
    ) -> _xr.DataArray:
        operation_type = self.settings.operation_type

        if operation_type is TimeOperationType.ADD:
            result = data.sum(dim=time_dim_name)

        elif operation_type is TimeOperationType.MIN:
            result = data.min(dim=time_dim_name)

        elif operation_type is TimeOperationType.MAX:
            result = data.max(dim=time_dim_name)

        elif operation_type is TimeOperationType.AVERAGE:
            result = data.mean(dim=time_dim_name)

        elif operation_type is TimeOperationType.MEDIAN:
            result = data.median(dim=time_dim_name)

        elif operation_type is TimeOperationType.STDEV:
            result = data.std(dim=time_dim_name)

        elif operation_type is TimeOperationType.PERCENTILE:
            result = data.quantile(
                self.settings.operation_parameter / 100, dim=time_dim_name
            ).drop_vars("quantile")

        else:
            raise NotImplementedError(
                f"The operation type '{operation_type}' " "is currently not supported"
            )

        return result
