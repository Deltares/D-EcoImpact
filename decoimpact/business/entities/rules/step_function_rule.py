import numpy as _np
import xarray as _xr

from decoimpact.business.entities.rules.cell_based_rule import CellBasedRule


class StepFunction(CellBasedRule):
    """Rule for Step function"""

    def __init__(
        self,
        name: str,
        input_variable_name: str,
        periods: list,
        intervals_limits: _np.array,
        interval_values: _np.array = None,
    ):
        super().__init__(name, input_variable_name)

        self._intervals_limits = intervals_limits
        self._interval_values = interval_values
        periods_dates = []

    def execute(self, date, value: float) -> float:
        """Classify a variable, based on given bins.
        Values lower than lowest bin will produce a warning and will be assigned calss 0.
        Values larger than the largest bin will produce a warning and will get the  highest bin index.

        Args:
            date (_type_): _description_
            value (float): value to classify

        Returns:
            float: index corresponding to value to classify
        """

        bins = self._limits

        # bins are constant
        if value < _np.min(bins):
            return bins[0]
        return _np.digitize(value, bins) - 1
