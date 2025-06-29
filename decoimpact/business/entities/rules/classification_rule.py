# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ClassificationRule class

Classes:
    ClassificationRule
"""

from typing import Dict, List, Optional

import xarray as _xr

from decoimpact.business.entities.rules.i_multi_array_based_rule import (
    IMultiArrayBasedRule,
)
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.business.entities.rules.string_parser_utils import (
    read_str_comparison,
    str_range_to_list,
    type_of_classification,
)
from decoimpact.crosscutting.i_logger import ILogger


class ClassificationRule(RuleBase, IMultiArrayBasedRule):
    """Implementation for the (multiple) classification rule"""

    def __init__(
        self,
        name: str,
        input_variable_names: List[str],
        criteria_table: Dict[str, List],
    ):
        super().__init__(name, input_variable_names)
        self._criteria_table = criteria_table

    @property
    def criteria_table(self) -> Dict:
        """Criteria property"""
        return self._criteria_table

    def execute(
        self, value_arrays: Dict[str, _xr.DataArray], logger: ILogger
    ) -> _xr.DataArray:
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

        for row, out in reversed(list(enumerate(self._criteria_table["output"]))):
            criteria_comparison = _xr.full_like(value_arrays[column_names[0]], True)
            for column_name in column_names:
                # DataArray on which the criteria needs to be checked
                data = value_arrays[column_name]

                # Retrieving criteria and applying it in correct format (number,
                # range or comparison)
                criteria = self.criteria_table[column_name][row]
                comparison = self._get_comparison_for_criteria(criteria, data)
                if comparison is None:
                    comparison = True

                # Criteria_comparison == 1 -> to check where the value is True
                criteria_comparison = _xr.where(
                    comparison & (criteria_comparison == 1), True, False
                )
            # For the first row set the default to None, for all the other
            # rows use the already created dataarray
            default_val = None
            if row != len(self._criteria_table["output"]) - 1:
                default_val = result_array

            result_array = _xr.where(criteria_comparison, out, default_val)
        return result_array

    def _get_comparison_for_criteria(
        self, criteria: str, data: _xr.DataArray
    ) -> Optional[_xr.DataArray]:

        criteria_class = type_of_classification(criteria)

        comparison = None
        if criteria_class == "number":
            comparison = data == float(criteria)

        elif criteria_class == "range":
            begin, end = str_range_to_list(criteria)
            comparison = (data >= begin) & (data <= end)

        elif criteria_class == "larger_equal":
            comparison_val = read_str_comparison(criteria, ">=")
            comparison = data >= float(comparison_val)

        elif criteria_class == "smaller_equal":
            comparison_val = read_str_comparison(criteria, "<=")
            comparison = data <= float(comparison_val)

        elif criteria_class == "larger":
            comparison_val = read_str_comparison(criteria, ">")
            comparison = data > float(comparison_val)

        elif criteria_class == "smaller":
            comparison_val = read_str_comparison(criteria, "<")
            comparison = data < float(comparison_val)

        return comparison
