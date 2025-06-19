# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
    Module for StepFunction class

Classes:
    StepFunction

"""

from typing import List

import numpy as _np

from decoimpact.business.entities.rules.i_cell_based_rule import ICellBasedRule
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.crosscutting.i_logger import ILogger


class StepFunctionRule(RuleBase, ICellBasedRule):
    """Rule for Step function

    Defines a step function output (float) to an input (float).

    The input sorted list [limit_1, limit_2, ..., limit_i, ..., limit_n]
    where limit_1 < limit_2 < ... < limit_i < ... < limit_n
    defines the limits of the interval for which the output values apply.

    f(val) = f(limit_i) if  limit_i<= val < limit_(i+1), no warning message is logged.
    f(val) = f(limit_1) if val = limit_1, no warning message is logged.
    f(val) = f(limit_1) if val < limit_1, and a warning message is logged.
    f(val) = f(limit_n) if val = limit_n, no warning message is logged.
    f(val) = f(limit_n) if val > limit_n, and a warning message is logged.

    """

    def __init__(
        self,
        name: str,
        input_variable_name: str,
        limits: List[float],
        responses: List[float],
    ):
        super().__init__(name, [input_variable_name])

        self._limits = _np.array(limits)
        self._responses = _np.array(responses)

    @property
    def limits(self):
        """Limits property"""
        return self._limits

    @property
    def responses(self):
        """Responses property"""
        return self._responses

    def validate(self, logger: ILogger) -> bool:
        if len(self._limits) != len(self._responses):
            logger.log_error("The number of limits and of responses must be equal.")
            return False
        if len(self._limits) != len(set(self._limits)):
            logger.log_error("Limits must be unique.")
            return False
        if not (self._limits == _np.sort(self._limits)).all():
            logger.log_error("The limits should be given in a sorted order.")
            return False
        return True

    def execute(self, value: float, logger: ILogger):
        """Classify a variable, based on given bins.
        Values lower than lowest bin will produce a warning and will
        be assigned class 0.
        Values larger than the largest bin will produce a warning
        and will get the highest bin index.

        Args:
            date (_type_): _description_
            value (float): value to classify

        Returns:
            float: response corresponding to value to classify
            int[]: number of warnings less than minimum and greater than maximum
        """

        bins = self._limits
        responses = self._responses

        # bins are constant
        selected_bin = -1
        warning_counter = [0, 0]
        if _np.isnan(value):
            return value, warning_counter
        if value < _np.min(bins):
            # count warning exceeding min:
            warning_counter[0] = 1
            selected_bin = 0
        else:
            selected_bin = _np.digitize(value, bins) - 1
            if value > _np.max(bins):
                # count warning exceeding max:
                warning_counter[1] = 1

        return responses[selected_bin], warning_counter
