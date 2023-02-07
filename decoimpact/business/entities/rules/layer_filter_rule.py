"""
Module for LayerFilterRule interface

Classes:
    LayerFilterRule
"""

from typing import List

import xarray as _xr

from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.rule_base import RuleBase


class LayerFilterRule(RuleBase, IArrayBasedRule):

    """Rule for filtering by layer number"""

    def __init__(
        self,
        name: str,
        input_variable_names: List[str],
        layer_number: int,
    ):
        super().__init__(name, input_variable_names)
        self._layer_number = layer_number

    @property
    def layer_number(self) -> int:
        """Name of the rule"""
        return self._layer_number

    def execute(self, value_array: _xr.DataArray) -> _xr.DataArray:

        """Obtain a 2D layer from a 3D variable

        Args:
            value (float): 3D value to obtain a layer from


        Returns:
            float: 2D variable
        """
        return value_array[:, :, self._layer_number - 1]
