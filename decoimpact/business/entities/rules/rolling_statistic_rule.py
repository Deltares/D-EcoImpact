# This file is part of D-EcoImpact
# Copyright (C) 2022-2023  Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the GNU
# Lesser General Public License version 2.1
# A copy of the GNU General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for RollingStatisticRule class

Classes:
    RollingStatisticRule
"""

import copy as _cp
import datetime as _dt

# from itertools import groupby
from typing import List

import numpy as _np
import xarray as _xr
from xarray.core.resample import DataArrayResample

from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.time_operation_type import TimeOperationType
from decoimpact.data.dictionary_utils import get_dict_element


class RollingStatisticRule(RuleBase, IArrayBasedRule):
    """Implementation for the rolling statistic rule"""

    def __init__(
        self,
        name: str,
        input_variable_names: List[str],
        operation_type: TimeOperationType,
        time_scale: str = "day", #TODO: why day?
        period: float = 5.2, #TODO: why 5.2
        output_variable_name: str = "output",
        description: str = "",
    ):
        super().__init__(name, input_variable_names, output_variable_name, description)
        self._operation_type = operation_type
        self._time_scale = time_scale.lower()
        self._time_scale_mapping = {"hour": "H", "day": "D", "month": "M", "year": "Y"} #TODO: shall we have this dictionary somewhere else?
        self._period = period

    @property
    def operation_type(self):
        """Operation type property"""
        return self._operation_type

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

        """Aggregates the values for the specified start and end date

        Args:
            value_array (DataArray): value to aggregate

        Returns:
            DataArray: Aggregated values 
        """
        #TODO: check if the comment is relevant.
        dim_name = get_dict_element(self._time_scale, self._time_scale_mapping) #TODO: this could be replaced if we replace the line with the dictionary above
        

        time_dim_name = self._get_time_dimension_name(value_array, logger) 

        result = self._perform_operation(
            value_array,
            time_dim_name,
            self._period,
            dim_name,
            logger,
        )
        return result

    def _perform_operation(
        self,
        values: _xr.DataArray,
        time_dim_name: str,
        period: float,
        dim_name: str,
        logger: ILogger,
    ) -> _xr.DataArray:
        """Returns the values based on the operation type

        Args:
            aggregated_values (DataArrayResample): aggregate values

        Raises:
            NotImplementedError: If operation type is not supported

        Returns:
            DataArray: Values of operation type
        """
        # derived from this stackoverflow answer:
        # https://stackoverflow.com/questions/76556088/rolling-timedelta-temporal-window-with-xarray

        result_array = _cp.deepcopy(values)
        result_array = result_array.where(False, _np.nan)

        if dim_name == "H":
            TMAXdt = _dt.timedelta(hours=period) #TODO: TMAXdt meaning?
        elif dim_name == "D":
            TMAXdt = _dt.timedelta(days=period)
        elif dim_name == "M":
            TMAXdt = _dt.timedelta(months=period)
        elif dim_name == "Y":
            TMAXdt = _dt.timedelta(years=period)
        else:
            logger.log_error(f"Invalid dim_name provided : '{dim_name}'.")

        TMAX = _np.array([TMAXdt], dtype="timedelta64[ms]")[0]
        last_timestamp = values.time.isel(time=-1).values
        for t in values.time.values:  # Interested in vectorizing this loop

            if last_timestamp - t < TMAX:
                break
            data = values.sel(time=slice(t, t + TMAX))
            last_timestamp_data = data.time.isel(time=-1).values

            if self._operation_type is TimeOperationType.ADD:
                result = data.sum(dim="time")

            if self._operation_type is TimeOperationType.MIN:
                result = data.min(dim="time")

            if self._operation_type is TimeOperationType.MAX:
                result = data.max(dim="time")

            if self._operation_type is TimeOperationType.AVERAGE:
                result = data.mean(dim="time")

            if self._operation_type is TimeOperationType.MEDIAN:
                result = data.median(dim="time")

            if self._operation_type is TimeOperationType.STDEV:
                result = data.std(dim="time")
           
            """ elif self._operation_type is TimeOperationType.PERCENTILE:
                result = data.quantile(
                    self._operation_parameter / 100
                ).drop_vars("quantile")
            """
            if result is None:
                raise NotImplementedError(
                    f"The operation type '{self._operation_type}' "
                    "is currently not supported"
                )

            # result_array.loc[dict(time=t + TMAX)] = result
            result_array.loc[dict(time=last_timestamp_data)] = result

        return _xr.DataArray(result_array)
    #TODO: move the function below to utils
    def _get_time_dimension_name(self, variable: _xr.DataArray, logger: ILogger) -> str:
        """Retrieves the dimension name

        Args:
            value_array (DataArray): values to get time dimension

        Raises:
            ValueError: If time dimension could not be found

        Returns:
            str: time dimension name
        """

        for dim in variable.dims:
            dim_values = variable[dim]
            if dim_values.dtype.name == "datetime64[ns]":
                return str(dim)

        message = f"No time dimension found for {variable.name}"
        logger.log_error(message)
        raise ValueError(message)
