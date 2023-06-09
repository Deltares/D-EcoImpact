"""
Module for ClassificationRule class

Classes:
    ClassificationRule
"""

from typing import Dict, List

import xarray as _xr

from decoimpact.business.entities.rules.i_multi_cell_based_rule import (
    IMultiCellBasedRule,
)
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.crosscutting.i_logger import ILogger


class ClassificationRule(RuleBase, IMultiCellBasedRule):
    """Implementation for the (multiple) classification rule"""

    def __init__(
        self,
        name: str,
        input_variable_names: List[str],
        criteria_table: Dict[str, List],
        output_variable_name: str = "output",
        description: str = "",
    ):
        super().__init__(name, input_variable_names, output_variable_name, description)
        self._criteria_table = criteria_table

    @property
    def criteria_table(self) -> Dict:
        """Criteria property"""
        return self._criteria_table

    def execute(self, values: Dict[str, float], logger: ILogger) -> int:

        """Determine the classification based on the table with criteria
        Args:
            values (Dict[str, float]): Dictionary holding the values
                                         for making the rule
        Returns:
            integer: classification
        """
        rows = len(self._criteria_table["output"])
        output_result = None
        # TODO: add ranges comparison
        # TODO: check existance of output column
        # TODO: do we always expect floats?
        criteria_comparison = None
        for r in range(rows):

            criteria_comparisons = []
            for par_name, par_values in self._criteria_table.items():
                if par_name != "output":
                    if par_values[r] == '-':
                        criteria_comparison = True
                    else:
                        criteria_comparison = values[par_name] == par_values[r]
                    criteria_comparisons.append(criteria_comparison)

            if all(criteria_comparisons):
                output_result = self._criteria_table["output"][r]
        
        # if there are multiple classifications we return the last one for now
        return output_result
