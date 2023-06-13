"""
Module for MultiplyRule class

Classes:
    MultiplyRule
"""

from typing import List

import xarray as _xr
import numpy as np

from datetime import date, datetime
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
        output_variable_name: str = "output",
        date_range: List[List[str]] = [],
        description: str = "",
    ):
        super().__init__(name, input_variable_names, output_variable_name, description)
        self._multipliers = multipliers
        self._date_range = date_range

    @property
    def multipliers(self) -> List[List[float]]:
        """Multiplier property"""
        return self._multipliers

    @property
    def date_range(self) -> List[List[str]]:
        """Date range property"""
        return self._date_range

    def execute(self, value_array: _xr.DataArray, logger: ILogger) -> _xr.DataArray:
        """Multiplies the value with the specified multipliers. If there is no date range,
        multiply the whole DataArray with the same multiplier. If there is table format with
        date range, make sure that the correct values in time are multiplied with the
        corresponding multipliers.
        Args:
            value_array (DataArray): values to multiply
        Returns:
            DataArray: Multiplied values
        """
        # Per time period multiple multipliers can be given, reduce this to
        # one multiplier by taking the product of all multipliers.
        result_multipliers = [np.prod(mp) for mp in self._multipliers]
        dr = _xr.DataArray(value_array)

        for (index, multiplier) in enumerate(result_multipliers):
            if (len(self.date_range) != 0):
                # Date is given in DD-MM, convert to MM-DD for comparison
                start = datetime.strptime(self.date_range[index][0], r"%d-%m")
                start = start.strftime(r"%m-%d")
                end = datetime.strptime(self.date_range[index][1], r"%d-%m")
                end = end.strftime(r"%m-%d")
                dr_date = dr.time.dt.strftime(r"%m-%d")
                dr = _xr.where((start < dr_date) & (dr_date < end), dr * multiplier, dr)
            else:
                dr = dr * multiplier
        return dr
