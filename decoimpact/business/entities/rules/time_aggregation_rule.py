"""
Module for TimeAggregationRule interface

Classes:
    TimeAggregationRule
"""

from typing import List

import xarray as _xr

from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.operation_type import OperationType
from decoimpact.business.entities.rules.rule_base import RuleBase


class TimeAggregationRule(RuleBase, IArrayBasedRule):
    """Implementation for the time aggregation rule"""

    def __init__(
        self,
        name: str,
        input_variable_names: List[str],
        operation_type: OperationType,
        time_scale: str = "year",
        output_variable_name: str = "output",
        description: str = "",
    ):
        super().__init__(name, input_variable_names, output_variable_name, description)
        self._operation_type = operation_type
        self._time_scale = time_scale

    def execute(self, value_array: _xr.DataArray) -> _xr.DataArray:

        """Aggregates the values for the specified start and end date

        Args:
            value_array (DataArray): value to aggregate

        Returns:
            DataArray: Aggregated values
        """

        if self._time_scale == "month":
            dim_name = "M"
        else:
            dim_name = "Y"

        time_dim_name = self._get_time_dimension_name(value_array)
        if time_dim_name is None:
            raise ValueError(f"No time dimension found for {value_array.name}")

        aggregated_values = value_array.resample({time_dim_name: dim_name})

        result = self._perform_operation(aggregated_values)
        # create a new aggregated time dimension based on original
        # time dimension
        result_time_dim_name = f"{time_dim_name}_{self._time_scale}"
        result = result.rename({time_dim_name: result_time_dim_name})

        for key, value in value_array[time_dim_name].attrs.items():
            if value:
                result[result_time_dim_name].attrs[key] = value

        return result

    def _perform_operation(self, aggregated_values: _xr.DataArray) -> _xr.DataArray:
        if self._operation_type is OperationType.MULTIPLY:
            return _xr.DataArray(aggregated_values.sum())

        if self._operation_type is OperationType.MIN:
            return _xr.DataArray(aggregated_values.min())

        if self._operation_type is OperationType.MAX:
            return _xr.DataArray(aggregated_values.max())

        if self._operation_type is OperationType.AVERAGE:
            return _xr.DataArray(aggregated_values.mean())

        if self._operation_type is OperationType.MEDIAN:
            return _xr.DataArray(aggregated_values.median())

    def _get_time_dimension_name(self, variable: _xr.DataArray) -> str:

        for dim in variable.dims:
            dim_values = variable[dim]
            if dim_values.dtype.name == "datetime64[ns]":
                return dim