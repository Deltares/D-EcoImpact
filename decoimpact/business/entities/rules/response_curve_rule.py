# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for Response Curve Rule class

Classes:
    Response Curve Rule
"""

from typing import List

import numpy as _np

from decoimpact.business.entities.rules.i_cell_based_rule import ICellBasedRule
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.crosscutting.i_logger import ILogger


class ResponseCurveRule(RuleBase, ICellBasedRule):
    """Rule for response function"""

    def __init__(
        self,
        name: str,
        input_variable_name: str,
        input_values: List[float],
        output_values: List[float],
    ):
        super().__init__(name, [input_variable_name])

        self._input_values = _np.array(input_values)
        self._output_values = _np.array(output_values)

    @property
    def input_values(self):
        """Input values property"""
        return self._input_values

    @property
    def output_values(self):
        """Output values property"""
        return self._output_values

    def validate(self, logger: ILogger) -> bool:
        if len(self._input_values) != len(self._output_values):
            logger.log_error("The input and output values must be equal.")
            return False
        if not (self._input_values == _np.sort(self._input_values)).all():
            logger.log_error("The input values should be given in a sorted order.")
            return False
        return True

    def execute(self, value: float, logger: ILogger):
        """Interpolate a variable, based on given input and output values.
        Values lower than lowest value will be set to NaN, values larger than
        the highest value will be set to NaN

        Args:
            value (float): value to classify
            input_values (_np.array): input values to use
            output_values (_np.array): output values to use

        Returns:
            float: response corresponding to value to classify
            int[]: number of warnings less than minimum and greater than maximum
        """

        values_input = self._input_values
        values_output = self._output_values
        warning_counter = [0, 0]

        # values are constant
        if value < _np.min(values_input):
            # count warning exceeding min:
            warning_counter[0] = 1
            return values_output[0], warning_counter

        if value > _np.max(values_input):
            # count warning exceeding max:
            warning_counter[1] = 1
            return values_output[-1], warning_counter

        return _np.interp(value, values_input, values_output), warning_counter
