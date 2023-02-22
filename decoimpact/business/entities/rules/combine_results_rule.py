"""
Module for CombineResultsRule Class

Classes:
    CombineResultsRule
"""


from typing import List

import numpy as _np
import xarray as _xr

from decoimpact.business.entities.rules.i_multi_array_based_rule import (
    IMultiArrayBasedRule,
)
from decoimpact.business.entities.rules.multi_array_operation_type import (
    MultiArrayOperationType,
)
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.crosscutting.i_logger import ILogger


class CombineResultsRule(RuleBase, IMultiArrayBasedRule):
    """Implementation for the combine results rule"""

    def __init__(
        self,
        name: str,
        input_variable_names: List[str],
        operation_type: MultiArrayOperationType,
        output_variable_name: str,
    ):
        super().__init__(name, input_variable_names, output_variable_name)
        self._operation_type = operation_type

    @property
    def operation_type(self) -> MultiArrayOperationType:
        """Name of the rule"""
        return self._operation_type

    def execute(
        self, value_arrays: List[_xr.DataArray], logger: ILogger
    ) -> _xr.DataArray:
        """Calculate simple statistic variables from two/more input arrays
        Args:
            input_arrays (DataArray): array list  containing the variables
        Returns:
            DataArray: Input arrays
        """

        np_arrays = [a_array.to_numpy() for a_array in value_arrays]

        if not self._check_dimensions(np_arrays):
            raise ValueError("The arrays are not in the same dimension/shape!")

        if self._operation_type is MultiArrayOperationType.MULTIPLY:
            result = np_arrays[0]

            for a_array in np_arrays[1:]:
                result = _np.multiply(result, a_array)

            return _xr.DataArray(result)
        # notice: multiply, we mean all the array multiply with the
        # all arrays, number by number.

        if self._operation_type is MultiArrayOperationType.MIN:
            return _xr.DataArray(_np.min(np_arrays, axis=0))

        if self._operation_type is MultiArrayOperationType.MAX:
            return _xr.DataArray(_np.max(np_arrays, axis=0))

        if self._operation_type is MultiArrayOperationType.AVERAGE:
            return _xr.DataArray(_np.average(np_arrays, axis=0))

        if self._operation_type is MultiArrayOperationType.MEDIAN:
            return _xr.DataArray(_np.median(np_arrays, axis=0))

        if self._operation_type is MultiArrayOperationType.ADD:
            result = np_arrays[0]

            for a_array in np_arrays[1:]:
                result = _np.add(result, a_array)

            return _xr.DataArray(result)
        # notice: Add, we mean all the array add with the all arrays, number by number.

        if self._operation_type is MultiArrayOperationType.SUBTRACT:
            result = np_arrays[0]

            for a_array in np_arrays[1:]:
                result = _np.subtract(result, a_array)

            return _xr.DataArray(result)

        raise NotImplementedError("The operation from input is not implemented")
        # notice: Subtract, we mean all the array Subtract with the all
        # arrays, number by number.

    def _check_dimensions(self, np_arrays: List[_np.array]) -> bool:
        """Brief check if all the arrays to be combined are in the
           same size/dimension/length
        Args:
            np_arrays: List of numpy arrays
        Returns:
            Boolean: True of False
        """

        expected_dimensions = np_arrays[0].ndim

        for a_array in np_arrays[1:]:
            if expected_dimensions != _np.ndim(a_array):
                return False

        expected_shape = np_arrays[0].shape
        for a_array in np_arrays[1:]:
            if expected_shape != a_array.shape:
                return False

        return True
