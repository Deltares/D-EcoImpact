"""
Module for LayerFilterRule class

Classes:
    LayerFilterRule
"""

from typing import List

import xarray as _xr

from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.crosscutting.i_logger import ILogger


class LayerFilterRule(RuleBase, IArrayBasedRule):

    """Implementation for the layer filter rule"""

    def __init__(
        self,
        name: str,
        input_variable_names: List[str],
        layer_number: int,
        layer_name: str = "nLayers",
        output_variable_name: str = "output",
        description: str = "",
    ):
        super().__init__(name, input_variable_names, output_variable_name, description)
        self._layer_number = layer_number
        self._layer_name = layer_name

    @property
    def layer_number(self) -> int:
        """Layer number property"""
        return self._layer_number

    @property
    def layer_name(self) -> str:
        """Layer number property"""
        return self._layer_name

    def execute(self, value_array: _xr.DataArray, logger: ILogger) -> _xr.DataArray:

        """Obtain a 2D layer from a 3D variable

        Args:
            value (float): 3D value to obtain a layer from


        Returns:
            float: 2D variable
        """

        if self._layer_name not in value_array.dims:
            message = f"""Layer name is not in dim names \
                [{value_array.dims}] layer_name [{self._layer_name}]"""
            logger.log_error(message)
            raise IndexError(message)

        dim_name = self._layer_name

        if not (
            self._layer_number >= 0
            and self._layer_number <= len(getattr(value_array, dim_name))
        ):
            message = f"""Layer number should be within range \
                [0,{len(getattr(value_array, dim_name))}]"""
            logger.log_error(message)
            raise IndexError(message)

        return value_array[:, :, self._layer_number - 1]
