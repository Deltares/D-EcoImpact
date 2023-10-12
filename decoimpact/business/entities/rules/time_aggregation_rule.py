# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for TimeAggregationRule class

Classes:
    TimeAggregationRule
"""

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


class TimeAggregationRule(RuleBase, IArrayBasedRule):
    """Implementation for the time aggregation rule"""

    def __init__(
        self,
        name: str,
        input_variable_names: List[str],
        operation_type: TimeOperationType,
        operation_parameter: float,
        time_scale: str = "year",
        output_variable_name: str = "output",
        description: str = "",
    ):
        super().__init__(name, input_variable_names, output_variable_name, description)
        self._operation_type = operation_type
        self._operation_parameter = operation_parameter
        self._time_scale = time_scale.lower()
        self._time_scale_mapping = {"month": "M", "year": "Y"}

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
        """Aggregates the values for the specified start and end date

        Args:
            value_array (DataArray): value to aggregate

        Returns:
            DataArray: Aggregated values
        """
        if self._operation_type is TimeOperationType.COUNT_PERIODS:
            # Check if all values in a COUNT_PERIODS value array are either 0 or 1
            compare_values = (value_array == 0) | (value_array == 1)
            check_values = _xr.where(compare_values, True, False)
            if False in check_values:
                raise ValueError(
                    "The value array for the time aggregation rule with operation type"
                    " COUNT_PERIODS should only contain the values 0 and 1."
                )

        dim_name = get_dict_element(self._time_scale, self._time_scale_mapping)

        time_dim_name = self._get_time_dimension_name(value_array, logger)
        aggregated_values = value_array.resample({time_dim_name: dim_name})

        result = self._perform_operation(aggregated_values)
        # create a new aggregated time dimension based on original time dimension

        result_time_dim_name = f"{time_dim_name}_{self._time_scale}"
        result = result.rename({time_dim_name: result_time_dim_name})

        for key, value in value_array[time_dim_name].attrs.items():
            if value:
                result[result_time_dim_name].attrs[key] = value

        result = result.assign_coords(
            {result_time_dim_name: result[result_time_dim_name]}
        )
        result[result_time_dim_name].attrs["long_name"] = result_time_dim_name
        result[result_time_dim_name].attrs["standard_name"] = result_time_dim_name

        return result

    def _perform_operation(self, aggregated_values: DataArrayResample) -> _xr.DataArray:
        """Returns the values based on the operation type

        Args:
            aggregated_values (DataArrayResample): aggregate values

        Raises:
            NotImplementedError: If operation type is not supported

        Returns:
            DataArray: Values of operation type
        """
        period_operations = [
            TimeOperationType.COUNT_PERIODS,
            TimeOperationType.MAX_DURATION_PERIODS,
            TimeOperationType.AVG_DURATION_PERIODS,
        ]

        if self._operation_type is TimeOperationType.ADD:
            result = aggregated_values.sum()

        elif self._operation_type is TimeOperationType.MIN:
            result = aggregated_values.min()

        elif self._operation_type is TimeOperationType.MAX:
            result = aggregated_values.max()

        elif self._operation_type is TimeOperationType.AVERAGE:
            result = aggregated_values.mean()

        elif self._operation_type is TimeOperationType.MEDIAN:
            result = aggregated_values.median()

        elif self._operation_type in period_operations:
            result = aggregated_values.reduce(self.analyze_groups, dim="time")

        elif self._operation_type is TimeOperationType.STDEV:
            result = aggregated_values.std()

        elif self._operation_type is TimeOperationType.PERCENTILE:
            result = aggregated_values.quantile(
                self._operation_parameter / 100
            ).drop_vars("quantile")

        elif self._operation_type is TimeOperationType.QUANT10:
            result = aggregated_values.quantile(0.1).drop_vars("quantile")

        elif self._operation_type is TimeOperationType.QUANT90:
            result = aggregated_values.quantile(0.9).drop_vars("quantile")

        else:
            raise NotImplementedError(
                f"The operation type '{self._operation_type}' "
                "is currently not supported"
            )

        return _xr.DataArray(result)

    # def quantile(self, q: float):
    #     """Method to determine quantile

    #     Args: quantile: the value q th to pass on to the quantile function
    #     """
    #     return aggregated_values.quantile(q).drop_vars("quantile")

    def count_groups(self, elem):
        """
        Count the amount of times the groups of 1 occur.

        Args:
            elem (Array): the data array in N-dimensions

        Returns:
            List: list with the counted periods
        """
        # in case of an example array with 5 values [1,1,0,1,0]:
        # subtract last 4 values from the first 4 values: [1,0,1,0] - [1,1,0,1]:
        # (the result of this example differences: [0,-1,1,0])
        differences = _np.diff(elem)
        # First add the first element of the array to the difference array (as this
        # could also indicate a beginning of a group or not and the diff is calculated
        # from the second element)
        # when the difference of two neighbouring elements is 1, this indicates the
        # start of a group. to count the number of groups: count the occurences of
        # difference == 1: (the result of this examples: 1 + 1 = 2)
        differences = _np.append(differences, elem[0])
        return _np.count_nonzero(differences == 1)

    def duration_groups(self, elem):
        """
        Create an array that cumulative sums the values of the groups in the array,
        but restarts when a 0 occurs. For example: [0, 1, 1, 0, 1, 1, 1, 0, 1]
        This function will return: [0, 1, 2, 0, 1, 2, 3, 0, 1, 2, 0, 1]

        Args:
            elem (List): the data array in N-dimensions

        Returns:
            List: List with the duration of the periods
        """
        # Function to create a cumsum over the groups (where the elements in elem are 1)
        cumsum_groups = _np.frompyfunc(lambda a, b: a + b if b == 1 else 0, 2, 1)
        return cumsum_groups.accumulate(elem)

    def analyze_groups(self, elem, axis, **kwargs):
        """This function analyzes the input array (N-dimensional array containing 0
        and 1) The function will reduce the array over the time axis, depending on a
        certain time operation type. Below are the operation types with what this
        function will do to this example input array: [0, 1, 1, 0, 1, 0]. A period
        is all consecutive 1 values.
            - COUNT_PERIODS: count the amount of periods (result: 2)
            - MAX_DURATION_PERIODS: gives the longest period (result: 2)
            - AVG_DURATION_PERIODS: gives the average of periods (result: 1.5)

        Args:
            elem (Array): the data array in N-dimensions
            axis (integer): the value describing the time axis

        Returns:
            array: array with the analyzed periods, with the same dimensions as elem
        """
        no_axis = len(_np.shape(elem))

        # The reduce function that calls this analyze_groups function should be reduces
        # over the time axis. The argument axis in this function gives a number of which
        # axis is in fact the time axis. This axis needs to move to the last position,
        # because we need to reduce the N-dimensional arary to a 1D array with all the
        # values in time for a specific cell in order to do the calculation for that
        # cell. Because we are looping over the N-dimensional array iteratively, we
        # should only move the time axis the first time this function is called (so when
        # the axis is not yet set to -1!)
        if axis != -1:
            elem = _np.moveaxis(elem, axis, -1)
            axis = -1

        #  in case of 1 dimension:
        if no_axis == 1:
            if self._operation_type is TimeOperationType.COUNT_PERIODS:
                group_result = self.count_groups(elem)
            elif self._operation_type is TimeOperationType.MAX_DURATION_PERIODS:
                group_result = _np.max((self.duration_groups(elem)))
            elif self._operation_type is TimeOperationType.AVG_DURATION_PERIODS:
                period = float(_np.sum(elem))
                group_count = float(self.count_groups(elem))
                group_result = _np.divide(
                    period,
                    group_count,
                    out=_np.zeros_like(period),
                    where=group_count != 0,
                )

        # in case of multiple dimensions:
        else:
            group_result = []
            for sub_elem in elem:
                # loop through this recursive function, determine output per axis:
                group_result_row = self.analyze_groups(sub_elem, axis)
                # add the result to the list of results, per axis:
                group_result.append(group_result_row)

        return group_result

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
