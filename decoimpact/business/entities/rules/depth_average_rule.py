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
from typing import List

import xarray as _xr

from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.crosscutting.i_logger import ILogger


class DepthAverageRule(RuleBase, IArrayBasedRule):
    """Implementation for the depthaverage rule"""

    def __init__(
        self,
        name: str,
        # variable_vertical_coordinates: str = 'mesh2d_interface_z',
        input_variable_names: List[str],
    ):
        super().__init__(name, input_variable_names)

    def execute(self, value_array: _xr.DataArray, logger: ILogger) -> _xr.DataArray:
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
        variable_vertical_coordinates = "mesh2d_interface_z"
        depths = value_array.variables[variable_vertical_coordinates]
        # QUESTION: is this variables with coordinates available this way?

        # assemble array with heights of each layer (and add it to output)
        # assumption: input array starts with bottom and works to top
        # for example [-7,-2,-1] where -7=bottom and 0=surface
        layer_heights = _xr.DataArray()
        # loop through layers and calculate heigth:
        for i in range(len(depths)):
            if i < len(depths) - 1:
                next_depth = depths[i + 1]
            else:
                next_depth = 0
            height = depths[i] - next_depth
            layer_heights.append(height)
        # TO DO: add this to output

        # multiply value with size to get relative value

        # determine total size of vertical dimensions

        # calculate depth average (use xarray for best performance)
        result_average = _xr.DataArray()  # (this is a place holder)

        return result_average
