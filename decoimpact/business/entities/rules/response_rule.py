from typing import List

import numpy as _np
import xarray as _xr

from decoimpact.business.entities.rules.i_cell_based_rule import ICellBasedRule
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.crosscutting.i_logger import ILogger


class ResponseRule(RuleBase, ICellBasedRule):

    """Rule for response function"""

    def __init__(
        self,
        name: str,
        input_variable_name: str,
        input_values: List[float],
        output_values: List[float],
        output_variable_name="output",
    ):

        super().__init__(name, [input_variable_name], output_variable_name)

        self._name = name
        self._input_variable_names[0] = input_variable_name
        self._input_values = _np.array(input_values)
        self._output_values = _np.array(output_values)

    def validate(self, logger: ILogger) -> bool:
        if len(self._input_values) != len(self._output_values):
            logger.log_error("The input and output values must be equal.")
            return False
        if not (self._input_values == _np.sort(self._input_values)).all():
            logger.log_error("The input values should be given in a sorted order.")
            return False
        return True

    def execute(self, value: float, logger: ILogger) -> float:

        """Interpolate a variable, based on given input and output values.
        Values lower than lowest value will be set to NaN, values larger than the highest value will be set to NaN

        Args:
            value (float): value to classify
            input_values (_np.array): input values to use
            output_values (_np.array): output values to use

        Returns:
            float: response corresponding to value to classify
        """

        values_input = self._input_values
        values_output = self._output_values

        # values are constant
        if value < _np.min(values_input):
            logger.log_warning("value less than min")
            return values_output[0]

        if value > _np.max(values_input):
            logger.log_warning("value greater than max")
            return values_output[-1]

        return _np.interp(value, values_input, values_output)
