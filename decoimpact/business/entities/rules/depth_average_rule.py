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

        # TO DO: calculate depth average
        # Use setup of the time_aggregation_rule.
        # Define the name of the depth dimension
        # resamplen not needed
        # _perform_operation should be adapted/integrated into execute for only DEPTH_AVERAGE
        # use the volume based average (take depth differences into account as well as dry/wet cells)

        # For calculation -> array based (use functionality of xarray for the performance)
        # 1. Calculate layer depth and add as a serperate varaiable
        # 2. Calculate average over depth
        # Same output!
        dr = _xr.DataArray(value_array)

        return dr
