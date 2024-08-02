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
from decoimpact.crosscutting.delft3d_specific_data import (
    BED_LEVEL_SUFFIX,
    INTERFACES_Z_SUFFIX,
    WATER_LEVEL_SUFFIX,
)
from decoimpact.crosscutting.i_logger import ILogger


class DepthAverageRule(RuleBase, IMultiArrayBasedRule):
    """Implementation for the depth average rule"""

    def execute(
        self, value_arrays: Dict[str, _xr.DataArray], logger: ILogger
    ) -> _xr.DataArray:
        """Calculate depth average of assumed z-layers.

        Args:
            value_array (DataArray): Values to average over the depth

        Returns:
            DataArray: Depth-averaged values
        """

        # The first DataArray in our value_arrays contains the values to be averaged
        # but the name of the key is given by the user, and is unknown here, so
        # just use the first value.
        variables = next(iter(value_arrays.values()))

        bed_level_values = self._extract_variable_based_on_suffix(
            value_arrays, BED_LEVEL_SUFFIX)
        depths_interfaces = self._extract_variable_based_on_suffix(
            value_arrays, INTERFACES_Z_SUFFIX)
        water_level_values = self._extract_variable_based_on_suffix(
            value_arrays, WATER_LEVEL_SUFFIX)

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

        # Deal with open layer system at water level and bed level
        depths_interfaces.values[depths_interfaces.values.argmin()] = -100000
        depths_interfaces.values[depths_interfaces.values.argmax()] = 100000

        # Broadcast the depths to the dimensions of the bed levels. Then make a
        # correction for the depths to the bed level, in other words all depths lower
        # than the bed level will be corrected to the bed level.
        depths_interfaces_broadcasted = depths_interfaces.broadcast_like(
            bed_level_values
        )

        corrected_depth_bed = depths_interfaces_broadcasted.where(
            bed_level_values < depths_interfaces_broadcasted, bed_level_values
        )

        # Make a similar correction for the waterlevels (first broadcast to match
        # dimensions and then replace all values higher than waterlevel with
        # waterlevel)
        corrected_depth_bed = corrected_depth_bed.broadcast_like(water_level_values)
        corrected_depth_bed = corrected_depth_bed.where(
            water_level_values > corrected_depth_bed, water_level_values
        )

        # Calculate the layer heights between depths
        layer_heights = corrected_depth_bed.diff(dim=dim_interfaces_name)
        layer_heights = layer_heights.rename({dim_interfaces_name: dim_layer_name})

        # Use the NaN filtering of the variables to set the correct depth per column
        layer_heights = layer_heights.where(variables.notnull())

        # Calculate depth average using relative value
        relative_values = variables * layer_heights

        # Calculate average
        return relative_values.sum(dim=dim_layer_name) / layer_heights.sum(
            dim=dim_layer_name
        )

    def _extract_variable_based_on_suffix(
            self,
            value_arrays: Dict[str, _xr.DataArray],
            suffix: str
            ) -> list:
        """Extract the values from the XArray dataset based on the name
        suffixes by matching the name, irrespective of the dummy name prefix.

        Args:
            value_array (DataArray): Values
            suffix (str) : Suffix of the name

        Returns:
            values (List[str]): Values based on prefix + suffix name
        """
        variable = [value_arrays[name] for name in value_arrays if suffix in name][0]
        return variable
