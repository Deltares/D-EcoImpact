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
        # variable_vertical_coordinates: str = 'mesh2d_interface_z',
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

        # get array with vertical dimensions (=depths) of layers
        #   :vertical_dimensions = mesh2d_nLayers: mesh2d_nInterfaces
        #   --> mesh2d_interface_z(mesh2d_nInterfaces=23)
        # TO DO: how to retrieve this?
        # variable_vertical_coordinates = "mesh2d_interface_z"

        print(value_arrays)
        print(value_arrays.keys())
        # values_over_height = value_arrays[0].sum(dim="mesh2d_nLayers")
        # total_heights = value_arrays[1].sum(dim="mesh2d_nLayers")
        # print(value_arrays)
        # depths = value_arrays[variable_vertical_coordinates].values
        # QUESTION: is this variable with coordinates available this way?

        # assemble array with heights of each layer (and add it to output)
        # assumption: input array starts with bottom and works to top (=0)
        # for example [-7,-2,-1] where -7=bottom and 0=surface
        # TO DO: check whether depths are starting at the bottom?
        # layer_heights = []
        # # loop through layers and calculate heigth:
        # for i, depth in enumerate(depths):
        #     if i < len(depths) - 1:
        #         next_depth = depths[i + 1]
        #     else:
        #         next_depth = 0
        #     height = depth - next_depth
        #     layer_heights.append(height)
        # # TO DO: add this to output

        # # calculate depth average using relative value
        # relative_values = value_array * layer_heights
        # depth_average = relative_values / sum(layer_heights)
        # # QUESTION: how to deal with rounding? is it better to use the min(depths)?

        return value_arrays["salinity"]
