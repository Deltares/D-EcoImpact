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

    def execute(
        self, value_arrays: Dict[str, _xr.DataArray], logger: ILogger
    ) -> _xr.DataArray:
        """Calculate depth average of assumed z-layers.
        Args:
            value_array (DataArray): Values to multiply
        Returns:
            DataArray: Averaged values
        """
        interface_name = "mesh2d_interface_z"
        water_level_name = "mesh2d_s1"
        bed_level_name = "mesh2d_flowelem_bl"

        dim_layer_name = "mesh2d_nLayers"
        dim_interfaces_name = "mesh2d_nInterfaces"

        # The first DataArray in our value_arrays contains the values to be averaged
        # But the name of the key is given by the user, so just take the first
        variables = next(iter(value_arrays.values()))

        # depths interfaces = borders of the layers in terms of depth
        depths_interfaces = value_arrays[interface_name]
        water_level_values = value_arrays[water_level_name]
        bed_level_values = value_arrays[bed_level_name]

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
        corrected_depths = corrected_depth_bed.where(
            water_level_values > corrected_depth_bed, water_level_values
        )

        # Calculate the layer heights between depths
        layer_heights = corrected_depths.diff(dim=dim_interfaces_name)
        layer_heights = layer_heights.rename({dim_interfaces_name: dim_layer_name})

        # Use the nan filtering of the variables to set the correct depth per column
        heights_all_filtered = layer_heights.where(variables.notnull())

        # Calculate depth average using relative value
        relative_values = variables * heights_all_filtered

        # Calculate total height and total value in column
        sum_relative_values = relative_values.sum(dim=dim_layer_name)
        sum_heights = heights_all_filtered.sum(dim=dim_layer_name)

        # Calculate average
        depth_average = sum_relative_values / sum_heights

        return depth_average
