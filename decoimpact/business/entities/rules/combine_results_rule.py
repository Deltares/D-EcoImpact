"""
Module for CombineResultsRule interface

Classes:
    CombineResultsRule
"""


from typing import Any, List

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

    @property
    def operation_type(self) -> OperationType:
        """Name of the rule"""
        return self._operation_type

    def execute(self, input_arrays: List[_xr.DataArray]) -> _xr.DataArray:
        # type: ignore
        """Calculate simple statistic variables from two/more input arrays
        Args:
            input_arrays (DataArray): array list  containing the variables
        Returns:
            DataArray: Input arrays
        """

        # if self._operation_type.value > 7:
        #    raise ValueError(f"Unsupported operation type {self._operation_type.name}")

        np_arrays = [a_array.to_numpy() for a_array in input_arrays]

        if not self._check_dimentions(np_arrays):
            raise ValueError(
                f"The arrays are not in the same dimension {self.input_variable_names}"
            )

        if self._operation_type is OperationType.Multiply:
            result = np_arrays[0]

            for a_array in np_arrays[1:]:
                result = _np.multiply(result, a_array)

            return _xr.DataArray(result)
        # notice: multiply, we mean all the array multiply with the all arrays, number by number.

        if self._operation_type is OperationType.Min:
            result = np_arrays[0]

            for a_array in np_arrays:
                result = _np.minimum(result, a_array)

            return _xr.DataArray(result)

        if self._operation_type is OperationType.Max:
            result = np_arrays[0]

            for a_array in np_arrays:
                result = _np.maximum(result, a_array)

            return _xr.DataArray(result)

        if self._operation_type is OperationType.Average:
            np_arrays = [a_array.to_numpy() for a_array in input_arrays]
            return _xr.DataArray(_np.average(np_arrays, axis=0))

        if self._operation_type is OperationType.Median:
            np_arrays = [a_array.to_numpy() for a_array in input_arrays]
            return _xr.DataArray(_np.median(np_arrays, axis=0))

        if self._operation_type is OperationType.Add:
            result = np_arrays[0]

            for a_array in np_arrays[1:]:
                result = _np.add(result, a_array)

            return _xr.DataArray(result)
        # notice: Add, we mean all the array add with the all arrays, number by number.

        if self._operation_type is OperationType.Substract:
            result = np_arrays[0]

            for a_array in np_arrays[1:]:
                result = _np.subtract(result, a_array)

            return _xr.DataArray(result)
        # notice: Substract, we mean all the array Substract with the all arrays, number by number.

    def _check_dimentions(self, np_arrays: List[_np.array]) -> bool:
        # brief check if all the arrays to be combined are in the same size/dimension/length
        expected_dimentions = np_arrays[0].ndim

        for a_array in np_arrays[1:]:
            if expected_dimentions != _np.ndim(a_array):
                return False

        expected_shape = np_arrays[0].shape
        for a_array in np_arrays[1:]:
            if expected_shape != a_array.shape:
                return False

        return True
