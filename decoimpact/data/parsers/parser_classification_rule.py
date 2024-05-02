# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ParserClassificationRule class

Classes:
    ParserClassificationRule
"""
from typing import Any, Dict
import numpy as _np

from decoimpact.business.entities.rules.string_parser_utils import (
    read_str_comparison,
    str_range_to_list,
    type_of_classification,
)
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import convert_table_element, get_dict_element
from decoimpact.data.entities.classification_rule_data import ClassificationRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.validation_utils import validate_table_with_input


class ParserClassificationRule(IParserRuleBase):
    """Class for creating a ClassificationRuleData"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "classification_rule"

    def parse_dict(self, dictionary: Dict[str, Any], logger: ILogger) -> IRuleData:
        """Parses the provided dictionary to a IRuleData
        Args:
            dictionary (Dict[str, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            RuleBase: Rule based on the provided data
        """
        name = get_dict_element("name", dictionary)
        input_variable_names = get_dict_element("input_variables", dictionary)
        criteria_table_list = get_dict_element("criteria_table", dictionary)
        criteria_table = convert_table_element(criteria_table_list)

        validate_table_with_input(criteria_table, input_variable_names)
        self._validate_criteria_on_overlap_and_gaps(criteria_table, logger)

        output_variable_name = get_dict_element("output_variable", dictionary)
        description = get_dict_element("description", dictionary)

        return ClassificationRuleData(
            name,
            input_variable_names,
            criteria_table,
            output_variable_name,
            description,
        )

    def _validate_criteria_on_overlap_and_gaps(self, criteria_table, logger: ILogger):
        for name, criteria in criteria_table.items():
            if name == "output":
                continue

            overlap_msg = []
            gap_msg = []

            not_covered_values = [-_np.inf, _np.inf]
            covered_numbers = []

            all_criteria = [type_of_classification(val) for val in criteria]
            # Check if there are multiple larger or larger and equal comparison values are present, this will cause overlap
            if all_criteria.count('larger') + all_criteria.count('larger_equal') > 1: 
                overlap_msg.append(f"Overlap for variable {name}, multiple criteria with > or >= values are defined")

            # Check if there are multiple larger or larger and equal comparison values are present, this will cause overlap
            if all_criteria.count('smaller') + all_criteria.count('smaller_equal') > 1: 
                overlap_msg.append(f"Overlap for variable {name}, multiple criteria with operators < or <= are defined")

            # First set the bounds of the criteria range, by checking if there are both > (or >=) and < (or <=) are present. Without these there will always be a gap defined.

            # Check upper bound (> and >=)

            for bnd_name, operator in [("larger_equal", ">="), ("larger", ">")]:
                for val in (
                    c for c in criteria if (type_of_classification(c) == bnd_name) or
                ):
                    comparison_val = read_str_comparison(val, operator)
                    if not_covered_values[-1] > comparison_val:
                        not_covered_values[-1] = comparison_val
                        if bnd_name == "larger_equal":
                            covered_numbers.append(comparison_val)

            # for val in (c for c in criteria if (type_of_classification(c) == "larger")):
            #     comparison_val = read_str_comparison(val, ">")
            #     if not_covered_values[-1] > comparison_val:
            #         not_covered_values[-1] = comparison_val

            # Check lower bound (< and <=)
            for bnd_name, operator in [("smaller_equal", "<="), ("smaller", "<")]:
                for val in (
                    c for c in criteria if (type_of_classification(c) == bnd_name)
                ):
                    comparison_val = read_str_comparison(val, operator)
                    if not_covered_values[0] < comparison_val:
                        not_covered_values[0] = comparison_val
                        if bnd_name == "smaller_equal":
                            covered_numbers.append(comparison_val)

            # If the upperbound is lower than the lower bound there is an overlap
            # For example when the user defines >10 and <100 -> not_covered_values will look like: [100, 10] and there is an overlap between 10 and 100. But all values are covered. So empty not_covered_values array.
            if not_covered_values[0] > not_covered_values[-1]:
                overlap_msg.append(
                    f"Overlap for variable {name} in range {not_covered_values[-1]}:{not_covered_values[0]}"
                )
                not_covered_values = []

            # If the upper and lowerbound are the same. And this value is covered in the covered_numbers array: empty the not_covered_values array, all values are covered. For example the user defines >0 and <=0 -> not_covered_values will look like: [0, 0] and the covered_numbers array: [0].
            if not_covered_values[0] == not_covered_values[-1]:
                not_covered_values = []

            # If not_covered_values is empty, it means all values are covered. All other defined criteria will cause an overlap.
            if len(not_covered_values) == 0:
                for comparison_string in ["number", "range"]:
                    for val in (
                        val
                        for val in criteria
                        if (type_of_classification(val) == comparison_string)
                    ):
                        overlap_msg.append(
                            f"Overlap for variable {name} in  {comparison_string}: {val}"
                        )

            # If not_covered_values is not empty, the other criteria might fill these gaps. First check on the numbers.
            else:
                not_covered_values = [not_covered_values]
                for val in (
                    c for c in criteria if (type_of_classification(c) == "number")
                ):
                    for not_covered_range in not_covered_values:
                        start, end = not_covered_range[0], not_covered_range[-1]
                        if self._check_inside_bounds(start, end, float(val)):
                            # If number is inside the bounds, split up the array into 2 ranges and add to covered_numbers
                            # If the number is the same/ or outside the bound, leave as is and add to covered_numbers => overlap





                for val in (
                    c for c in criteria if (type_of_classification(c) == "range")
                ):
                    start_range, end_range = str_range_to_list(val)

                    for not_covered_range in not_covered_values:
                        start, end = not_covered_range[0], not_covered_range[-1]
                        begin_inside = self._check_inside_bounds(start, end, start_range)
                        end_inside = self._check_inside_bounds(start, end, end_range)
                        if begin_inside & end_inside:
                            # The range is inside the not covered values eg when the user gives the criteria: <=0, >10 and 3:5, making two serperate gaps.

                            # The range is outside the covered values eg when the user gives the criteria: <=0, >10 and 13:15, overlap

                            # The range starts within the bounds eg when the user gives the criteria: <=0, >10 and 3:15, an overlap and a gap

                            # The range ends within the bounds eg when the user gives the criteria: <=0, >10 and -3:5, an overlap and a gap

                            # The range is larger than the given bounds 
                            # The range starts within the bounds eg when the user gives the criteria: <=0, >10 and -3:15. All values covered, but overlap


            # Create the final check over the not_covered_values and the covered_numbers
            # Send warning with the combined messages
            print("\n".join(overlap_msg))
            print("\n".join(gap_msg))
            # Only show the first 10 lines. Print all warnings to a txt file.

    def _check_inside_bounds(self, start, end, var):
        return (var > start) & (var < end)