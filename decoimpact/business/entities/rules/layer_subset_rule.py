"""
Module for LayerFilterRule class

Classes:
    LayerFilterRule
"""

from typing import List

import numpy as _np
import xarray as _xr

from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.crosscutting.i_logger import ILogger


class LayerSubsetRule(RuleBase, IArrayBasedRule):

    """Implementation for the layer subset rule"""

    def __init__(
        self,
        name: str,
        input_variable_names: List[str],
        start_layer_number: int,
        end_layer_number: int,
        layer_name: str = "nLayers",
        output_variable_name: str = "output",
        description: str = "",
    ):
        super().__init__(name, input_variable_names, output_variable_name, description)
        self._start_layer_number = start_layer_number
        self._end_layer_number = end_layer_number
        self._layer_name = layer_name

    @property
    def start_layer_number(self) -> int:
        """Start Layer number property"""
        return self._start_layer_number

    @property
    def end_layer_number(self) -> int:
        """End Layer number property"""
        return self._end_layer_number

    @property
    def layer_name(self) -> str:
        """Layer number property"""
        return self._layer_name

    def execute(self, value_array: _xr.DataArray, logger: ILogger) -> _xr.DataArray:

        """Obtain a selection of a layer from a variable

        Args:
            value (float): variable to obtain a layer from


        Returns:
            float: subset of variable
        """

        if self._layer_name not in value_array.dims:
            message = f"""Layer name is not in dim names \
                [{value_array.dims}] layer_name [{self._layer_name}]"""
            logger.log_error(message)
            raise IndexError(message)

        dim_name = self._layer_name

        if not (
            self._start_layer_number >= 0
            and self._start_layer_number <= len(getattr(value_array, dim_name))
        ):
            message = f"""Start layer number should be within range \
                [0,{len(getattr(value_array, dim_name))}]"""
            logger.log_error(message)
            raise IndexError(message)

        if not (
            self._end_layer_number >= 0
            and self._end_layer_number <= len(getattr(value_array, dim_name))
        ):
            message = f"""End layer number should be within range \
                [0,{len(getattr(value_array, dim_name))}]"""
            logger.log_error(message)
            raise IndexError(message)
        
        dim_index = list(range(value_array.get_axis_num(dim_name),value_array[dim_name].size))
        mask = _xr.DataArray([dim_index_val < self._start_layer_number - 1 or\
              dim_index_val > self._end_layer_number - 1\
              for dim_index_val in dim_index], dims = [dim_name])
        return value_array.where(mask != 1, _np.nan)
        