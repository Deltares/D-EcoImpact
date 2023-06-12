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

    def str_range_to_list(self, s: str) -> List:
        """
        Convert a string with a range in the form "x:y" of floats to two elements (begin and end of range).
        """
        s = s.strip()
        try:
            begin, end = s.split(":")
            return float(begin), float(end)
        except ValueError:
            return print(f'Input "{s}" is not a valid range')

    def type_of_classification(self, s) -> str:
        """Determine which type of classification is required: number, range, or NA (not applicable)"""
        try:
            float(s)
            return "number"
        except:
            pass
        if ":" in s:
            return "range"
            # TODO: regexp gebruiken, controleren op: "GETAL:GETAL"
        if s == "-" or s == "":
            return "NA"

    def execute(self, values: Dict[str, float], logger: ILogger) -> int:
        """Determine the classification based on the table with criteria
        Args:
            values (Dict[str, float]): Dictionary holding the values
                                         for making the rule
        Returns:
            integer: classification
        """
        output_result = None
        # TODO: check existance of output column
        # TODO: do we always expect floats?
        # TODO: too many indices for array: array is 2-dimensional, but 3 were indexed (salinity)

        criteria_comparison = None
        # loop through all rules (=row)
        for r, outp in enumerate(self._criteria_table["output"]):
            criteria_comparisons = []
            # check all criteria (per rule)
            for par_name, par_values in self._criteria_table.items():
                # the output column can be ignored because it contains the result:
                if par_name == "output":
                    continue

                # determine type of criterium (range/value/ignore)
                if self.type_of_classification(par_values[r]) == "range":
                    min_val, max_val = str_range_to_list(par_values[r])
                    criteria_comparison = (
                        values[par_name] > min_val and values[par_name] < max_val
                    )
                elif self.type_of_classification(par_values[r]) == "number":
                    criteria_comparison = values[par_name] == par_values[r]
                elif self.type_of_classification(par_values[r]) == "NA":
                    criteria_comparison = True
                # add result of each equation to the list of criteria_comparisons = result list for one row/rule:
                criteria_comparisons.append(criteria_comparison)

            # if the results of all equation for one rule are true, then the rule applies:
            if all(criteria_comparisons):
                output_result = self._criteria_table["output"][r]

        # if there are multiple classifications we return the last one for now
        return output_result
