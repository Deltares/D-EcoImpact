"""
Module for LayerFilterRule class

Classes:
    LayerFilterRule
"""

from typing import List

import xarray as _xr

from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.rule_base import RuleBase


class LayerFilterRule(RuleBase, IArrayBasedRule):

    """Implementation for the layer filter rule"""

    def __init__(
        self,
        name: str,
        input_variable_names: List[str],
        layer_number: int,
        output_variable_name: str = "output",
        description: str = "",
    ):
        super().__init__(name, input_variable_names, output_variable_name, description)
        self._layer_number = layer_number

    @property
    def layer_number(self) -> int:
        """Layer number property"""
        return self._layer_number

    def execute(self, value_array: _xr.DataArray) -> _xr.DataArray:

        """Obtain a 2D layer from a 3D variable

        Args:
            value (float): 3D value to obtain a layer from


        Returns:
            float: 2D variable
        """

        if not (
            self._layer_number >= 0 and self._layer_number <= len(value_array.dims)
        ):
            message = (
                f"""Layer number should be within range [0,{len(value_array.dims)}]"""
            )
            raise IndexError(message)

        return value_array[:, :, self._layer_number - 1]
