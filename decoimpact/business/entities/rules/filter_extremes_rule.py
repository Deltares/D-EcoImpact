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

from typing import Any, List

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
        distance: List[Any],
        mask: bool,
    ):
        super().__init__(name, input_variable_names)
        self._extreme_type = extreme_type
        self._distance = distance
        self._mask = mask

    @property
    def extreme_type(self) -> str:
        """Type of extremes (peaks or troughs)"""
        return self._extreme_type

    @property
    def distance(self) -> List[any]:
        """Minimal distance between peaks"""
        return self._distance

    @property
    def mask(self) -> bool:
        """Return either directly the values of the filtered array or a
        True/False array"""
        return self._mask

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
        distance = width_time / timestep

        results = _xr.apply_ufunc(
            self._process_peaks,
            old_dr,
            input_core_dims=[[time_dim_name]],
            output_core_dims=[[time_dim_name]],
            vectorize=True,
            kwargs={"distance": distance, "mask": self.mask},
        )

        old_dims = list(old_dr.dims)
        # TODO: USE OLD_DIMS FOR TRANSPOSE!!!!
        results = results.transpose("time", "mesh2d_nFaces")
        return results

    def _process_peaks(self, arr: _xr.DataArray, distance: float, mask):
        peaks, _ = _sc.signal.find_peaks(arr, distance=distance)
        values = arr[peaks]
        if mask:
            values = True
        # TODO: use fill value of array
        new_arr = _np.full_like(arr, _np.NaN)
        new_arr[peaks] = values
        return new_arr
