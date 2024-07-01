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
from typing import Dict

import xarray as _xr

from decoimpact.business.entities.rules.i_multi_array_based_rule import (
    IMultiArrayBasedRule,
)
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.crosscutting.i_logger import ILogger


class DepthAverageRule(RuleBase, IMultiArrayBasedRule):
    """Implementation for the depthaverage rule"""

    def execute(
        self, value_arrays: Dict[str, _xr.DataArray], logger: ILogger
    ) -> _xr.DataArray:
        """Calculate depth average of assumed z-layers.
        Args:
            value_array (DataArray): Values to multiply
        Returns:
            DataArray: Averaged values
        """

        # The first DataArray in our value_arrays contains the values to be averaged
        # But the name of the key is given by the user, so just take the first
        variables = next(iter(value_arrays.values()))

        # depths interfaces = borders of the layers in terms of depth
        depths_interfaces = value_arrays["mesh2d_interface_z"]
        water_level_values = value_arrays["mesh2d_s1"]
        bed_level_values = value_arrays["mesh2d_flowelem_bl"]

        # Get the dimension names for the interfaces and for the layers
        dim_interfaces_name = list(depths_interfaces.dims)[0]
        interfaces_len = depths_interfaces[dim_interfaces_name].size

        dim_layer_name = [
            d for d in variables.dims if d not in water_level_values.dims
        ][0]
        layer_len = variables[dim_layer_name].size

        # interface dimension should always be one larger than layer dimension
        # Otherwise give an error to the user
        if interfaces_len != layer_len + 1:
            logger.log_error(
                f"The number of interfaces should be number of layers + 1. Number of"
                f"interfaces = {interfaces_len}. Number of layers = {layer_len}."
            )
            return variables

        # Broadcast the depths to the dimensions of the bed levels and
        # correct the depths to the bed level, in other words all depths lower
        # than bed level will be corrected to bed level.
        depths_interfaces_broadcasted = depths_interfaces.broadcast_like(
            bed_level_values
        )
        corrected_depth_bed = depths_interfaces_broadcasted.where(
            bed_level_values < depths_interfaces_broadcasted, bed_level_values
        )

        # Make a similiar correction for the waterlevels (first broadcast to match
        # dimensions and then replace all values higher than waterlevel with
        # waterlevel)
        corrected_depth_bed = corrected_depth_bed.broadcast_like(water_level_values)
        corrected_depth_bed = corrected_depth_bed.where(
            water_level_values > corrected_depth_bed, water_level_values
        )

        # Calculate the layer heights between depths
        layer_heights = corrected_depth_bed.diff(dim=dim_interfaces_name)
        layer_heights = layer_heights.rename({dim_interfaces_name: dim_layer_name})

        # Use the nan filtering of the variables to set the correct depth per column
        layer_heights = layer_heights.where(variables.notnull())

        # Calculate depth average using relative value
        relative_values = variables * layer_heights

        # Calculate average
        return relative_values.sum(dim=dim_layer_name) / layer_heights.sum(
            dim=dim_layer_name
        )
