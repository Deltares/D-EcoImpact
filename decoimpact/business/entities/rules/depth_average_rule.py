# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for DepthAverageRule class

Classes:
    DepthAverageRule
"""
from typing import Dict, List

import xarray as _xr

from decoimpact.business.entities.rules.i_multi_array_based_rule import (
    IMultiArrayBasedRule,
)
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.crosscutting.i_logger import ILogger


class DepthAverageRule(RuleBase, IMultiArrayBasedRule):
    """Implementation for the depthaverage rule"""

    def __init__(
        self,
        name: str,
        input_variable_names: List[str],
    ):
        super().__init__(name, input_variable_names)

    def validate(self, logger: ILogger) -> bool:
        return True

    def execute(
        self, value_arrays: Dict[str, _xr.DataArray], logger: ILogger
    ) -> _xr.DataArray:
        """Calculate depth average of assumed z-layers.
        Args:
            value_array (DataArray): Values to multiply
        Returns:
            DataArray: Averaged values
        """
        print(value_arrays)

        interface_name = "depth_interfaces"
        layer_name = "mesh2d_nLayers"

        # The first DataArray in our value_arrays contains the values to be averaged
        # But the name of the key is given by the user, so just take the first
        variables = next(iter(value_arrays.values()))
        # depths interfaces = borders of the layers in terms of depth
        depths_interfaces = value_arrays[interface_name]

        print("PRINT DEPTHS_INTERFACES:")
        print(depths_interfaces)
        print(depths_interfaces.values)

        # Calculate the layer heights between depths
        layer_heights = depths_interfaces.diff("mesh2d_nInterfaces")
        layer_heights = layer_heights.rename({"mesh2d_nInterfaces": "mesh2d_nLayers"})

        print("PRINT LAYER_HEIGHTS:")
        print(layer_heights)

        # Broadcast the heights in all dimensions
        heigths_all_dims = layer_heights.broadcast_like(variables)

        # Use the nan filtering of the variables to set the correct depth per column
        heights_all_filtered = heigths_all_dims.where(variables.notnull())

        # Calculate depth average using relative value
        relative_values = layer_heights.dot(
            variables
        )  # moet interface_name hier niet weg? hier heights_all_filtered ipv layer_heights?

        # Calculate total height and total value in column
        sum_relative_values = relative_values.sum(dim=layer_name)
        sum_heights = heights_all_filtered.sum(dim=layer_name)

        # Calculate average
        depth_average = sum_relative_values / sum_heights

        return depth_average
