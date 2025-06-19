# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for CombineResultsRule Class

Classes:
    CombineResultsRule
"""

from typing import Callable, Dict, List

import numpy as _np
import xarray as _xr

from decoimpact.business.entities.rules.i_multi_array_based_rule import (
    IMultiArrayBasedRule,
)
from decoimpact.business.entities.rules.options.multi_array_operation_type import (
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
    ):
        super().__init__(name, input_variable_names)
        self._operation_type: MultiArrayOperationType = operation_type
        self._operations = self._create_operations()

    @property
    def operation_type(self) -> MultiArrayOperationType:
        """Name of the rule"""
        return self._operation_type

    def validate(self, logger: ILogger) -> bool:
        if self._operation_type not in self._operations:

            message = (
                f"Operation type {self._operation_type} is currently" " not supported."
            )

            logger.log_error(message)
            return False

        if len(self._input_variable_names) < 2:
            logger.log_error("Minimum of two input variables required.")
            return False

        return True

    def execute(
        self, value_arrays: Dict[str, _xr.DataArray], logger: ILogger
    ) -> _xr.DataArray:
        """Calculate simple statistical operations with two or more input arrays
        Args:
            input_arrays (DataArray): array list containing the variables
        Returns:
            DataArray: Input arrays
        """
        if len(value_arrays) != len(self._input_variable_names):
            raise ValueError("Not all expected arrays where provided.")

        np_arrays = [a_array.to_numpy() for a_array in value_arrays.values()]
        if not self._check_dimensions(np_arrays):
            raise ValueError("The arrays must have the same dimensions.")

        operation_to_use = self._operations[self._operation_type]

        first_value_array = next(iter(value_arrays.values()))

        result_variable = _xr.DataArray(
            data=operation_to_use(np_arrays),
            dims=first_value_array.dims,
            attrs=first_value_array.attrs,
        )

        return result_variable

    def _create_operations(self) -> dict[MultiArrayOperationType, Callable]:
        return {
            MultiArrayOperationType.MULTIPLY: lambda npa: _np.prod(npa, axis=0),
            MultiArrayOperationType.MIN: lambda npa: _np.min(npa, axis=0),
            MultiArrayOperationType.MAX: lambda npa: _np.max(npa, axis=0),
            MultiArrayOperationType.AVERAGE: lambda npa: _np.average(npa, axis=0),
            MultiArrayOperationType.MEDIAN: lambda npa: _np.median(npa, axis=0),
            MultiArrayOperationType.ADD: lambda npa: _np.sum(npa, axis=0),
            MultiArrayOperationType.SUBTRACT: lambda npa: _np.subtract(
                npa[0], _np.sum(npa[1:], axis=0)
            ),
        }

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
