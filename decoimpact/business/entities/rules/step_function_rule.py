import numpy as _np

from decoimpact.business.entities.rules.I_cell_based_rule import ICellBasedRule
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.crosscutting.i_logger import ILogger


class StepFunction(RuleBase, ICellBasedRule):
    """Rule for Step function"""

    def __init__(
        self,
        name: str,
        input_variable_name: str,
        intervals_limits: _np.array,
        interval_values: _np.array = None,
    ):
        super().__init__(name, input_variable_name)

        self._name = name
        self._input_variable_name = input_variable_name
        self._intervals_limits = intervals_limits
        self._interval_values = interval_values

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

        bins = self._intervals_limits
        # bins are constant
        selected_bin = -1
        if value < _np.min(bins):
            logger.log_warning("value less than min")
            selected_bin = 0
        else:
            selected_bin = _np.digitize(value, bins) - 1
            if value > _np.max(bins):
                logger.log_warning("value greater than max")

        return self._interval_values[selected_bin]
