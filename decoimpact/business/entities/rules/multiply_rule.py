"""
Module for MultiplyRule interface

Classes:
    MultiplyRule
"""

from typing import List

import xarray as _xr

from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.rule_base import RuleBase


class MultiplyRule(RuleBase, IArrayBasedRule):
    """Implementation for the multiply rule"""

    def __init__(
        self, name: str, input_variable_names: List[str], multipliers: List[float]
    ):
        super().__init__(name, input_variable_names)
        self._multipliers = multipliers

    def execute(self, value_array: _xr.DataArray) -> _xr.DataArray:

        """Multiplies the value with the specified multipliers
        Args:
            value_array (DataArray): values to multiply
        Returns:
            DataArray: Multiplied values
        """

        result_multiplier = 1.0
        for multiplier in self._multipliers:
            result_multiplier = result_multiplier * multiplier

        return _xr.DataArray(value_array * result_multiplier)