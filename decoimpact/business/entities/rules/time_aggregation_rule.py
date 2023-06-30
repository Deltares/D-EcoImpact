"""
Module for TimeAggregationRule class

Classes:
    TimeAggregationRule
"""

# from itertools import groupby
from typing import List

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
        time_scale: str = "year",
        output_variable_name: str = "output",
        description: str = "",
    ):
        super().__init__(name, input_variable_names, output_variable_name, description)
        self._operation_type = operation_type
        self._time_scale = time_scale.lower()
        self._time_scale_mapping = {"month": "M", "year": "Y"}

    @property
    def operation_type(self):
        """Operation type property"""
        return self._operation_type

    @property
    def time_scale(self):
        """Time scale property"""
        return self.time_scale

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

        result = result.assign_coords({
            result_time_dim_name: result[result_time_dim_name]
        })
        result[result_time_dim_name].attrs['long_name'] = result_time_dim_name
        result[result_time_dim_name].attrs['standard_name'] = result_time_dim_name

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
        result = None
        if self._operation_type is TimeOperationType.ADD:
            result = aggregated_values.sum()

        if self._operation_type is TimeOperationType.MIN:
            result = aggregated_values.min()

        if self._operation_type is TimeOperationType.MAX:
            result = aggregated_values.max()

        if self._operation_type is TimeOperationType.AVERAGE:
            result = aggregated_values.mean()

        if self._operation_type is TimeOperationType.MEDIAN:
            result = aggregated_values.median()

        # if self._operation_type is TimeOperationType.COUNT_PERIODS:
        #     # result = self.count_groups(aggregated_values)
        #     av = _xr.DataArray(aggregated_values)
        #     result = self.count_groups(av)

        if result is None:
            raise NotImplementedError(
                f"The operation type '{self._operation_type}'"
                "is currently not supported"
            )

        return _xr.DataArray(result)

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
