# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for FilterExtremesRule class

Classes:
    FilterExtremesRule
"""

from typing import List

import xarray as _xr

from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.crosscutting.i_logger import ILogger


class FilterExtremesRule(RuleBase, IArrayBasedRule):
    """Implementation for the filter extremes rule"""

    def __init__(
        self,
        name: str,
        input_variable_names: List[str],
        extreme_type: str,
    ):
        super().__init__(name, input_variable_names)
        self._extreme_type = extreme_type

    @property
    def extreme_type(self) -> str:
        """Type of extremes (peaks or troughs)"""
        return self._extreme_type

    def execute(self, value_array: _xr.DataArray, logger: ILogger) -> _xr.DataArray:
        """Retrieve the peak or through values
        Args:
            value_array (DataArray): Values to filter at extremes
        Returns:
            DataArray: Filtered DataArray with only the extremes remaining
            at all other times the values are set to NaN
        """
        old_dr = _xr.DataArray(value_array)
        print(self._extreme_type)
        return old_dr
