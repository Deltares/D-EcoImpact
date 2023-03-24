from datetime import datetime

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
        periods: list,
        input_values: _np.array,
        output_values: _np.array,
        policies: _np.array = None,
        output_variable_name="output",
    ):

        super().__init__(name, [input_variable_name], output_variable_name)

        self._name = name
        self._input_variable_name = input_variable_name
        self._input_values = input_values
        self._output_values = output_values
        self._policies = policies
        period_dates = []

        for period in periods:
            startPeriod = datetime.strptime(period[0], "%d-%m").date()
            endPeriod = datetime.strptime(period[1], "%d-%m").date()
            period_dates.append([startPeriod, endPeriod])

        self._period_dates = period_dates

    def validate(self, logger: ILogger) -> bool:
        if len(self._input_values) != len(self._output_values):
            logger.log_error("The input and output values must be equal.")
            return False
        return True

    def execute(self, date, value: float) -> float:

        """Interpolate a variable, based on given input and output values.
        Values lower than lowest value will be set to NaN, values larger than the highest value will be set to NaN

        Args:
            value (float): value to classify
            input_values (_np.array): input values to use
            output_values (_np.array): output values to use

        Returns:
            indices: Index of classified value
        """
        values_input = self._input_values
        values_output = self._output_values

        if values_input.ndim == 1:
            # values are constant
            if value < _np.min(values_input):
                return _np.nan

            if value > _np.max(values_input):
                return _np.nan

            valuenew = _np.interp(value, values_input.tolist(), values_output.tolist())

        else:
            # values are time-dependent
            bin_index = 1
            bin_index = self._decide_bin(date)

            check_values_input = values_input[bin_index, :]
            check_values_input = check_values_input[
                check_values_input != _np.array(None)
            ]

            check_values_output = values_output[bin_index, :]
            check_values_output = check_values_output[
                check_values_output != _np.array(None)
            ]

            if value < _np.min(check_values_input):
                return _np.nan

            if value > _np.max(check_values_input):
                return _np.nan

            valuenew = _np.interp(
                value, check_values_input.tolist(), check_values_output.tolist()
            )

        return valuenew

    def after_execute(self, data: _xr.DataArray) -> _xr.DataArray:
        """Apply policies if defined"""
        if self._policies is None:
            return data

        return _xr.DataArray(self._policies[data.astype(float)])

    def _decide_bin(self, date) -> int:
        """Decide which bin to use. Ignores years, only checks for days and months"""

        date_to_check = datetime(1900, date[1], date[0]).date()

        index = 0
        for period_date in self._period_dates:
            start_period = period_date[0]
            end_period = period_date[1]

            if date_to_check >= start_period and date_to_check <= end_period:
                bin_index = index
                break

            index += 1

        # This does not check if multiple periods are overlapping.
        return bin_index

    def _set_year_to_1900(self, date):
        """Set year to 1900 to check with periods"""
        return date.replace(year=1900)
