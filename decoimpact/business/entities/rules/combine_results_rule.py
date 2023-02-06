"""
Module for CombineResultsRule interface

Classes:
    CombineResultsRule
"""


from typing import List

import numpy as _np
import xarray as _xr

from decoimpact.business.entities.rules.i_multi_array_based_rule import (
    IMultiArrayBasedRule,
)
from decoimpact.business.entities.rules.operation_type import OperationType
from decoimpact.business.entities.rules.rule_base import RuleBase


class CombineResultsRule(RuleBase, IMultiArrayBasedRule):
    """Implementation for the multiply rule"""

    def __init__(
        self, name: str, input_variable_names: List[str], operation_type: OperationType
    ):
        super().__init__(name, input_variable_names)
        self._operation_type = operation_type

    def execute(self, input_arrays: List[_xr.DataArray]) -> _xr.DataArray:
        # type: ignore
        """Calculate simple statistic variables from two/more input arrays
        Args:
            input_arrays (DataArray): array list  containing the variables
        Returns:
            DataArray: Input arrays
        """

        # variable1 = dataset[self.input_variable_name[0]]
        # variable2 = dataset[self.input_variable_name[1]]

        # if self._operation_type is OperationType.Multiply:
        #    return variable1 * variable2

        if self._operation_type.value > 5:
            raise ValueError(f"Unsupported operation type {self._operation_type.name}")

        # values1 = variable1.to_numpy()
        # values2 = variable2.to_numpy()

        np_arrays = [a.to_numpy() for a in input_arrays]

        if self._operation_type is OperationType.Multiply:
            result = np_arrays[0]

            for a in np_arrays:
                result = _np.multiply(result, a)

            return _xr.DataArray(result)
        # notice: multiply, we mean all the array multiply with the all arrays, number by number.

        if self._operation_type is OperationType.Min:
            result = np_arrays[0]

            for a in np_arrays:
                result = _np.minimum(result, a)

            return _xr.DataArray(result)

        if self._operation_type is OperationType.Max:
            result = np_arrays[0]

            for a in np_arrays:
                result = _np.maximum(result, a)

            return _xr.DataArray(result)

        if self._operation_type is OperationType.Average:
            np_arrays = [a.to_numpy() for a in input_arrays]
            return _xr.DataArray(_np.average(np_arrays, axis=0))

        if self._operation_type is OperationType.Median:
            np_arrays = [a.to_numpy() for a in input_arrays]
            return _xr.DataArray(_np.median(np_arrays, axis=0))
