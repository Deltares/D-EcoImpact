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
import scipy as _sc
import numpy as _np

from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.business.utils.data_array_utils import get_time_dimension_name
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
        time_dim_name = get_time_dimension_name(value_array, logger)
        # TODO: IF NO TIME AVAILABLE NOTIFY USER
        # TODO: implement extreme_type (peaks or troughs)
        # TODO: implement convertion of hours etc to width
        time = old_dr.time.values
        timestep = (time[-1] - time[0]) / len(time)
        width_time = _np.timedelta64(14, "D")
        width = width_time / timestep

        results = _xr.apply_ufunc(
            self._process_peaks,
            old_dr,
            input_core_dims=[[time_dim_name]],
            output_core_dims=[[time_dim_name]],
            vectorize=True,
            kwargs={"width": width},
        )
        return results

    def _process_peaks(self, arr: _xr.DataArray, width: float):
        peaks, _ = _sc.signal.find_peaks(arr, distance=width)
        # TODO: use fill value of array
        new_arr = _np.full_like(arr, -999)
        new_arr[peaks] = arr[peaks]
        return new_arr
