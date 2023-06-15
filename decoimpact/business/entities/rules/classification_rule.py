"""
Module for ClassificationRule class

Classes:
    ClassificationRule
"""

from typing import Dict, List

import xarray as _xr

from decoimpact.business.entities.rules.i_multi_array_based_rule import IMultiArrayBasedRule

from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.crosscutting.i_logger import ILogger


class ClassificationRule(RuleBase, IMultiArrayBasedRule):
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

    def str_range_to_list(self, range_string: str):
        """
        Convert a string with a range in the form "x:y" of floats to two elements (begin and end of range).
        """
        range_string = range_string.strip()
        try:
            begin, end = range_string.split(":")
            return float(begin), float(end)
        except ValueError:
            return print(f'Input "{s}" is not a valid range')

    def type_of_classification(self, class_val) -> str:
        """Determine which type of classification is required: number, range, or NA (not applicable)"""
        if type(class_val) == int or type(class_val) == float:
            return "number"
        elif type(class_val) == str:
            class_val = class_val.strip()
            if class_val == "-" or class_val == "":
                return "NA"
            if ":" in class_val:
                class_range = class_val.split(":")
                # len(class_range)
                return "range"
                # TODO: regexp gebruiken, controleren op: "GETAL:GETAL"
        return ""

    def execute(self,  value_arrays: Dict[str, _xr.DataArray], logger: ILogger) -> _xr.DataArray:
        """Determine the classification based on the table with criteria
        Args:
            values (Dict[str, float]): Dictionary holding the values
                                         for making the rule
        Returns:
            integer: classification
        """

        column_names = list(self._criteria_table.keys())
        column_names.remove("output")

        dr = _xr.DataArray(value_arrays[self.input_variable_names[0]]).copy()

        for (row, out) in enumerate(self._criteria_table["output"]):
            criteria_comparison = _xr.where(value_arrays[column_names[0]], True, True)
            for column_name in column_names:
                criteria = self.criteria_table[column_name][row]
                criteria_class = self.type_of_classification(criteria)
                data = value_arrays[column_name]
                if criteria_class == "number":
                    criteria_comparison = _xr.where(
                        (data == float(criteria)) & (criteria_comparison == True),
                        True,
                        False
                    )

            default_val = dr
            if (row == 0):
                default_val = None
            dr = _xr.where(criteria_comparison, out, default_val)
        print(dr)
        return dr

        # output_result = None
        # # TODO: check existance of output column
        # # TODO: do we always expect floats?
        # # TODO: too many indices for array: array is 2-dimensional, but 3 were indexed (salinity)

        # print(values)
        # criteria_comparison = None
        # # loop through all rules (=row)
        # for r, outp in enumerate(self._criteria_table["output"]):
        #     criteria_comparisons = []
        #     # check all criteria (per rule)
        #     for par_name, par_values in self._criteria_table.items():
        #         # the output column can be ignored because it contains the result:
        #         if par_name == "output":
        #             continue

        #         # determine type of criterium (range/value/ignore)
        #         if self.type_of_classification(par_values[r]) == "range":
        #             min_val, max_val = str_range_to_list(par_values[r])
        #             criteria_comparison = (
        #                 values[par_name] > min_val and values[par_name] < max_val
        #             )
        #         elif self.type_of_classification(par_values[r]) == "number":
        #             criteria_comparison = values[par_name] == par_values[r]
        #         elif self.type_of_classification(par_values[r]) == "NA":
        #             criteria_comparison = True
        #         # add result of each equation to the list of criteria_comparisons = result list for one row/rule:
        #         criteria_comparisons.append(criteria_comparison)

        #     # if the results of all equation for one rule are true, then the rule applies:
        #     if all(criteria_comparisons):
        #         output_result = self._criteria_table["output"][r]

        # # if there are multiple classifications we return the last one for now
        # return output_result
