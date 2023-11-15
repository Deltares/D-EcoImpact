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
from typing import List

import numpy as _np
import xarray as _xr

from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.business.utils.dataset_utils import get_time_dimension_name
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
        operation_parameter: float = 0,
        time_scale: str = "day",
        period: float = 1,
        output_variable_name: str = "output",
        description: str = "",
    ):
        super().__init__(name, input_variable_names, output_variable_name, description)
        self._operation_type = operation_type
        self._time_scale = time_scale.lower()
        self._operation_parameter = operation_parameter
        self._time_scale_mapping = {"hour": "H", "day": "D"}
        self._period = period

    @property
    def operation_type(self):
        """Operation type property"""
        return self._operation_type

    @property
    def operation_parameter(self):
        """Operation parameter property"""
        return self._operation_parameter

    @property
    def time_scale(self):
        """Time scale property"""
        return self._time_scale

    @property
    def time_scale_mapping(self):
        """Time scale mapping property"""
        return self._time_scale_mapping

    def validate(self, logger: ILogger) -> bool:
        """Validates if the rule is valid

        Returns:
            bool: wether the rule is valid
        """
        valid = True
        allowed_time_scales = self._time_scale_mapping.keys()

        if self._time_scale not in allowed_time_scales:
            options = ",".join(allowed_time_scales)
            logger.log_error(
                f"The provided time scale '{self._time_scale}' "
                f"of rule '{self._name}' is not supported.\n"
                f"Please select one of the following types: "
                f"{options}"
            )
            valid = False

        return valid

    def execute(self, value_array: _xr.DataArray, logger: ILogger) -> _xr.DataArray:
        """Calculating the rolling statistics for a given period

        Args:
            value_array (DataArray): value to aggregate

        Returns:
            DataArray: Aggregated values
        """

        time_scale = get_dict_element(self._time_scale, self._time_scale_mapping)

        time_dim_name = get_time_dimension_name(value_array, logger)

        result = self._perform_operation(
            value_array,
            time_dim_name,
            self._period,
            time_scale,
            logger,
        )
        return result

    def _perform_operation(
        self,
        values: _xr.DataArray,
        time_dim_name: str,
        period: float,
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
            operation_time_delta = _dt.timedelta(hours=period)
        elif time_scale == "D":
            operation_time_delta = _dt.timedelta(days=period)
        else:
            logger.log_error(f"Invalid time scale provided : '{time_scale}'.")

        time_delta_ms = _np.array([operation_time_delta], dtype="timedelta64[ms]")[0]
        last_timestamp = values.time.isel(time=-1).values
        for timestep in values.time.values:  # Interested in vectorizing this loop
            if last_timestamp - timestep < time_delta_ms:
                break
            data = values.sel(time=slice(timestep, timestep + time_delta_ms))
            last_timestamp_data = data.time.isel(time=-1).values

            if self._operation_type is TimeOperationType.ADD:
                result = data.sum(dim=time_dim_name)

            elif self._operation_type is TimeOperationType.MIN:
                result = data.min(dim=time_dim_name)

            elif self._operation_type is TimeOperationType.MAX:
                result = data.max(dim=time_dim_name)

            elif self._operation_type is TimeOperationType.AVERAGE:
                result = data.mean(dim=time_dim_name)

            elif self._operation_type is TimeOperationType.MEDIAN:
                result = data.median(dim=time_dim_name)

            elif self._operation_type is TimeOperationType.STDEV:
                result = data.std(dim=time_dim_name)

            elif self._operation_type is TimeOperationType.PERCENTILE:
                result = data.quantile(
                    self._operation_parameter / 100, dim=time_dim_name
                ).drop_vars("quantile")

            else:
                raise NotImplementedError(
                    f"The operation type '{self._operation_type}' "
                    "is currently not supported"
                )

            result_array.loc[{"time": last_timestamp_data}] = result

        return _xr.DataArray(result_array)
