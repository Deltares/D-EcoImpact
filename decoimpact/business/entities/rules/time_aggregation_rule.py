"""
Module for TimeAggregationRule class

Classes:
    TimeAggregationRule
"""

from typing import List

import xarray as _xr

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
        time_scale: str = "year",
        output_variable_name: str = "output",
        description: str = "",
    ):
        super().__init__(name, input_variable_names, output_variable_name, description)
        self._operation_type = operation_type
        self._time_scale = time_scale.lower()
        self._time_scale_mapping = {"month": "M", "year": "Y"}

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

        dim_name = get_dict_element(self._time_scale, self._time_scale_mapping)

        time_dim_name = self._get_time_dimension_name(value_array)
        if time_dim_name is None:
            message = f"No time dimension found for {value_array.name}"
            logger.log_error(message)
            raise ValueError(message)

        aggregated_values = value_array.resample({time_dim_name: dim_name})

        result = self._perform_operation(aggregated_values)
        # create a new aggregated time dimension based on original time dimension

        result_time_dim_name = f"{time_dim_name}_{self._time_scale}"
        result = result.rename({time_dim_name: result_time_dim_name})

        for key, value in value_array[time_dim_name].attrs.items():
            if value:
                result[result_time_dim_name].attrs[key] = value

        return result

    def _perform_operation(self, aggregated_values: _xr.DataArray) -> _xr.DataArray:
        """Returns the values based on the operation type

        Args:
            aggregated_values (DataArray): aggragetate values

        Returns:
            DataArray: Values of operation type
        """
        if self._operation_type is TimeOperationType.ADD:
            return _xr.DataArray(aggregated_values.sum())

        if self._operation_type is TimeOperationType.MIN:
            return _xr.DataArray(aggregated_values.min())

        if self._operation_type is TimeOperationType.MAX:
            return _xr.DataArray(aggregated_values.max())

        if self._operation_type is TimeOperationType.AVERAGE:
            return _xr.DataArray(aggregated_values.mean())

        if self._operation_type is TimeOperationType.MEDIAN:
            return _xr.DataArray(aggregated_values.median())

    def _get_time_dimension_name(self, variable: _xr.DataArray) -> str:
        """Retrieves the dimension name

        Args:
            value_array (DataArray): values to get time dimension

        Returns:
            str: time dimension name
        """

        for dim in variable.dims:
            dim_values = variable[dim]
            if dim_values.dtype.name == "datetime64[ns]":
                return dim
