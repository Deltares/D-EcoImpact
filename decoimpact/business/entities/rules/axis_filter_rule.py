# This file is part of D-EcoImpact
# Copyright (C) 2022-2025  Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the GNU
# Lesser General Public License version 2.1
# A copy of the GNU General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for AxisFilterRule class

Classes:
    AxisFilterRule
"""

from typing import List

import xarray as _xr

from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.crosscutting.i_logger import ILogger


class AxisFilterRule(RuleBase, IArrayBasedRule):
    """Implementation for the axis filter rule"""

    def __init__(
        self,
        name: str,
        input_variable_names: List[str],
        element_index: int,
        axis_name: str,
    ):
        super().__init__(name, input_variable_names)
        self._element_index = element_index
        self._axis_name = axis_name

    @property
    def element_index(self) -> int:
        """Value index of the provided axis to filter on"""
        return self._element_index

    @property
    def axis_name(self) -> str:
        """Layer number property"""
        return self._axis_name

    def execute(self, value_array: _xr.DataArray, logger: ILogger) -> _xr.DataArray:
        """Obtain a 2D layer from a 3D variable

        Args:
            value (float): 3D value to obtain a layer from


        Returns:
            float: 2D variable
        """

        if self._axis_name not in value_array.dims:
            message = f"""Layer name is not in dim names \
                [{value_array.dims}] layer_name [{self._axis_name}]"""
            logger.log_error(message)
            raise IndexError(message)

        if not (
            self._element_index >= 0
            and self._element_index <= len(getattr(value_array, self._axis_name))
        ):
            message = f"""Layer number should be within range \
                [0,{len(getattr(value_array, self._axis_name))}]"""
            logger.log_error(message)
            raise IndexError(message)

        return value_array.isel({self._axis_name: self._element_index - 1})
