"""
Module for ClassificationRule class

Classes:
    ClassificationRule
"""

from typing import Dict, List

import xarray as _xr

from decoimpact.business.entities.rules.i_multi_array_based_rule import IMultiArrayBasedRule

from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.business.entities.rules.string_parser_utils import (
    read_str_comparison,
    str_range_to_list,
    type_of_classification
)
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

    def execute(self,  value_arrays: Dict[str, _xr.DataArray], logger: ILogger) -> _xr.DataArray:
        """Determine the classification based on the table with criteria
        Args:
            values (Dict[str, float]): Dictionary holding the values
                                         for making the rule
        Returns:
            integer: classification
        """

        # Get all the headers in the criteria_table representing a value to be checked
        column_names = list(self._criteria_table.keys())
        column_names.remove("output")

        # Create an empty result_array to be filled
        result_array = _xr.zeros_like(value_arrays[column_names[0]])

        for (row, out) in reversed(list(enumerate(self._criteria_table["output"]))):
            criteria_comparison = _xr.full_like(value_arrays[column_names[0]], True)
            for column_name in column_names:
                # DataArray on which the criteria needs to be checked
                data = value_arrays[column_name]

                # Retrieving criteria and applying it in correct format (number, range or comparison)
                criteria = self.criteria_table[column_name][row]
                criteria_class = type_of_classification(criteria)

                comparison = True
                if criteria_class == "number":
                    comparison = data == float(criteria)

                elif criteria_class == "range":
                    begin, end = str_range_to_list(criteria)
                    comparison = (data > begin) & (data < end)

                elif criteria_class == "larger":
                    comparison_val = read_str_comparison(criteria, ">")
                    comparison = (data > float(comparison_val))

                elif criteria_class == "smaller":
                    comparison_val = read_str_comparison(criteria, "<")
                    comparison = (data < float(comparison_val))

                criteria_comparison = _xr.where(
                    comparison & (criteria_comparison == True),
                    True,
                    False
                )
            # For the first row set the default to None, for all the other
            # rows use the already created dataarray
            default_val = None
            if (row != len(self._criteria_table["output"])-1):
                default_val = result_array

            result_array = _xr.where(criteria_comparison, out, default_val)

        return result_array

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
