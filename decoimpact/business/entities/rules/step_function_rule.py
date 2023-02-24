"""
    Module for StepFunction class

Classes:
    StepFunction

    Defines a step function output (float) to an input (float).

    The input sorted list [limit_1, limit_2, ..., limit_i, ..., limit_n]
        where limit_1 < limit_2 < ... < limit_i < ... < limit_n
        defines the limits of the interval for which the output values apply.

        f(val) = f(limit_i) if  limit_i<= val < limit_(i+1)
        f(val) = f(limit_1) if val < limit_1, and a warning message is logged.
        f(val) = f(limit_n) if val > limit_1, and a warning message is logged.

"""

import numpy as _np

from decoimpact.business.entities.rules.i_cell_based_rule import ICellBasedRule
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.crosscutting.i_logger import ILogger


class StepFunctionRule(RuleBase, ICellBasedRule):
    """Rule for Step function

    The input sorted list [limit_1, limit_2, ..., limit_i, ..., limit_n]
    where limit_1 < limit_2 < ... < limit_i < ... < limit_n
    defines the limits of the interval for which the output values apply.

    f(val) = f(limit_i) if  limit_i<= val < limit_(i+1)
    f(val) = f(limit_1) if val < limit_1, and a warning message is logged.
    f(val) = f(limit_n) if val > limit_1, and a warning message is logged.

    """

    def __init__(
        self,
        name: str,
        input_variable_name: str,
        limits: _np.array,
        responses: _np.array,
        output_variable_name="output",
    ):
        super().__init__(name, [input_variable_name], output_variable_name)

        self._name = name
        self._input_variable_name = input_variable_name
        self._limits = limits
        self._responses = responses

    def validate(self, logger: ILogger) -> bool:
        if not len(self._limits) == len(self._responses):
            return False
        return True

    def execute(self, value: float, logger: ILogger) -> float:
        """Classify a variable, based on given bins.
        Values lower than lowest bin will produce a warning and will
        be assigned class 0.
        Values larger than the largest bin will produce a warning
        and will get the highest bin index.

        Args:
            date (_type_): _description_
            value (float): value to classify

        Returns:
            float: index corresponding to value to classify
        """

        bins = self._limits
        # bins are constant
        selected_bin = -1
        if value < _np.min(bins):
            logger.log_warning("value less than min")
            selected_bin = 0
        else:
            selected_bin = _np.digitize(value, bins) - 1
            if value > _np.max(bins):
                logger.log_warning("value greater than max")

        return self._responses[selected_bin]
