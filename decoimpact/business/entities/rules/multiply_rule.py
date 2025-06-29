# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for MultiplyRule class

Classes:
    MultiplyRule
"""

from datetime import datetime as _dt
from typing import List, Optional

import numpy as _np
import xarray as _xr

from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.crosscutting.i_logger import ILogger


class MultiplyRule(RuleBase, IArrayBasedRule):
    """Implementation for the multiply rule"""

    def __init__(
        self,
        name: str,
        input_variable_names: List[str],
        multipliers: List[List[float]],
        date_range: Optional[List[List[str]]] = None,
    ):
        super().__init__(name, input_variable_names)
        self._multipliers = multipliers
        self._date_range = date_range

    @property
    def multipliers(self) -> List[List[float]]:
        """Multiplier property"""
        return self._multipliers

    @property
    def date_range(self) -> Optional[List[List[str]]]:
        """Date range property"""
        return self._date_range

    def execute(self, value_array: _xr.DataArray, logger: ILogger) -> _xr.DataArray:
        """Multiplies the value with the specified multipliers. If there is no
        date range, multiply the whole DataArray with the same multiplier. If
        there is table format with date range, make sure that the correct values
        in time are multiplied with the corresponding multipliers.
        Args:
            value_array (DataArray): Values to multiply
        Returns:
            DataArray: Multiplied values
        """
        # Per time period multiple multipliers can be given, reduce this to
        # one multiplier by taking the product of all multipliers.
        result_multipliers = [_np.prod(mp) for mp in self._multipliers]
        old_dr = _xr.DataArray(value_array)
        new_dr = _xr.full_like(old_dr, _np.nan)

        for index, _mp in enumerate(result_multipliers):
            if self.date_range is not None and len(self.date_range) != 0:
                # Date is given in DD-MM, convert to MM-DD for comparison
                start = self._convert_datestr(self.date_range[index][0])
                end = self._convert_datestr(self.date_range[index][1])
                dr_date = old_dr.time.dt.strftime(r"%m-%d")
                new_dr = _xr.where(
                    (start < dr_date) & (dr_date < end), old_dr * _mp, new_dr
                )
            else:
                new_dr = old_dr * _mp
        return new_dr

    def _convert_datestr(self, date_str: str) -> str:
        parsed_str = _dt.strptime(date_str, r"%d-%m")
        return parsed_str.strftime(r"%m-%d")
