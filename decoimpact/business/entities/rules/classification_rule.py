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
        criteria: Dict[str, List],
        output_variable_name: str = "output",
        description: str = "",
    ):
        super().__init__(name, input_variable_names, output_variable_name, description)
        self._criteria = criteria

    @property
    def criteria(self) -> Dict:
        """Criteria property"""
        return self._criteria

    def execute(self, criteria: Dict[str, List], values: Dict[str, float], logger: ILogger) -> int:

        """Determine the classification based on the table with criteria
        Args:
            criteria (Dict[str, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            integer: classification
        """
        rows = len(criteria["output"])
        # print('rows:',rows)
        output_result = []

        rule = None
        for r in range(rows):
            print('--- row ', r)
            rules = []
            for par_name, par_values in criteria.items():
                if par_name != 'output':
                    # print(par_name, '=', par_values[r])
                    # TODO: change this below: we can never use 'r' (row) in relation to the values
                    rule = values[par_name][r] == par_values[r]
                    # print('value:',values[par_name][r],', par_value:', par_values[r], ', result:', rule)
                    rules.append(rule)
            # print('rules:',rules)
            if all(rules):
                output_result.append(criteria['output'][r])

        return output_result
