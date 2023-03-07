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
        description: str = "",
    ):
        super().__init__(name, input_variable_names, output_variable_name, description)
        self._operation_type: MultiArrayOperationType = operation_type

    @property
    def operation_type(self) -> MultiArrayOperationType:
        """Name of the rule"""
        return self._operation_type

    def execute(
        self, value_arrays: List[_xr.DataArray], logger: ILogger
    ) -> _xr.DataArray:
        """Calculate simple statistical operations with two or more input arrays
        Args:
            input_arrays (DataArray): array list containing the variables
        Returns:
            DataArray: Input arrays
        """
        np_arrays = [a_array.to_numpy() for a_array in value_arrays]
        if not self._check_dimensions(np_arrays):
            raise ValueError("The arrays must have the same dimensions.")

        operations = {
            MultiArrayOperationType.MULTIPLY: lambda npa: _np.product(npa, axis=0),
            MultiArrayOperationType.MIN: lambda npa: _np.min(npa, axis=0),
            MultiArrayOperationType.MAX: lambda npa: _np.max(npa, axis=0),
            MultiArrayOperationType.AVERAGE: lambda npa: _np.average(npa, axis=0),
            MultiArrayOperationType.MEDIAN: lambda npa: _np.median(npa, axis=0),
            MultiArrayOperationType.ADD: lambda npa: _np.sum(npa, axis=0),
            MultiArrayOperationType.SUBTRACT: lambda npa: _np.subtract(
                npa[0], _np.sum(npa[1:], axis=0)
            ),
        }
        result_variable = _xr.DataArray(
            data=operations[self._operation_type](np_arrays),
            dims=value_arrays[0].dims,
        )
        return result_variable  # result_array

    def _check_dimensions(self, np_arrays: List[_np.array]) -> bool:
        """Brief check if all the arrays to be combined have the
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
