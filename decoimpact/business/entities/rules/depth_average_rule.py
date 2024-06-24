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
        # variable_vertical_coordinates = "mesh2d_interface_z"

        # TODO:
        # - add comments
        # - make sure 'salinity' is not hardcoded, but use either first value from value_arrays or use a generic key here
        # -

        depths = value_arrays["mesh2d_interface_z"]

        layer_heights = depths.diff(dim="mesh2d_nInterfaces")

        # # calculate depth average using relative value
        relative_values = value_arrays["salinity"].dot(
            layer_heights, "mesh2d_nInterfaces"
        )
        sum_relative_values = relative_values.sum(dim="mesh2d_nLayers")

        # TODO: this goes wrong!! cannot sum layer_heights -> for every column different total height, because of dry cells!! do something smart with the nan cells in the salinity!
        depth_average = sum_relative_values / sum(layer_heights)
        print("hoi")
        print(sum(layer_heights).values)
        print(relative_values.values[1, 2328, :])
        print(sum_relative_values.values[1, 2328])
        print(depth_average.values[1, 2328])

        return depth_average
