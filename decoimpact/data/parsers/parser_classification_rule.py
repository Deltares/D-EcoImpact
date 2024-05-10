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
from bisect import insort, bisect_right, bisect_left

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

            not_covered_values = [-_np.inf, _np.inf]
            covered_numbers = []

            all_criteria = [type_of_classification(val) for val in criteria]
            # Check if there are multiple larger or larger and equal comparison values are present, this will cause overlap
            if all_criteria.count("larger") + all_criteria.count("larger_equal") > 1:
                overlap_msg.append(
                    f"Overlap for variable {name}, multiple criteria with operators > or >= are defined"
                )

            # Check if there are multiple larger or larger and equal comparison values are present, this will cause overlap
            if all_criteria.count("smaller") + all_criteria.count("smaller_equal") > 1:
                overlap_msg.append(
                    f"Overlap for variable {name}, multiple criteria with operators < or <= are defined"
                )

            # First set the bounds of the criteria range, by checking if there are both > (or >=) and < (or <=) are present. Without these there will always be a gap defined.

            # Check upper bound (> and >=)
            for bnd_name, operator in [("larger_equal", ">="), ("larger", ">")]:
                for val in (
                    c for c in criteria if (type_of_classification(c) == bnd_name)
                ):
                    comparison_val = read_str_comparison(val, operator)
                    if not_covered_values[-1] > comparison_val:
                        not_covered_values[-1] = comparison_val
                        if bnd_name == "larger_equal":
                            covered_numbers.append(comparison_val)

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
            if len(not_covered_values) != 0:
                if (not_covered_values[0] == not_covered_values[-1]) and (
                    not_covered_values[0] in covered_numbers
                ):
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
                            f"Overlap for variable {name} in {comparison_string}: {val}"
                        )

            # If not_covered_values is not empty, the other criteria might fill these gaps. First check on the numbers.
            else:
                new_not_covered_1 = [not_covered_values.copy()]
                for val in (
                    c for c in criteria if (type_of_classification(c) == "number")
                ):
                    for range_ind, not_covered_range in enumerate([not_covered_values]):
                        start, end = not_covered_range[0], not_covered_range[-1]
                        # If number is inside the bounds, split up the array into 2 ranges and add to covered_numbers
                        if self._check_inside_bounds(start, end, float(val)):
                            new_not_covered_1[range_ind] = [start, float(val)]
                            new_not_covered_1.insert(range_ind + 1, [float(val), end])

                        # If the number is the same/ or outside the bound, leave as is and add to covered_numbers => overlap
                        else:
                            covered_numbers.append(float(val))

                not_covered_values = new_not_covered_1
                for val in (
                    c for c in criteria if type_of_classification(c) == "range"
                ):
                    start_range, end_range = str_range_to_list(val)
                    print(f"HELLO, {val}")

                    not_covered_values, overlap_msg = self._check_new_range(
                        name, not_covered_values, start_range, end_range, overlap_msg
                    )

                    # if start == start_range:
                    #     overlap_msg.append(
                    #         f"Overlap for variable {name} at {start_range}"
                    #     )

                    # if end == end_range:
                    #     overlap_msg.append(
                    #         f"Overlap for variable {name} at {end_range}"
                    #     )

                for r in not_covered_values:
                    if (r[0] == r[-1]) & (r[0] not in covered_numbers):
                        overlap_msg.append(f"Gap for variable {name} in number {r[0]}")
                    if r[0] != r[-1]:
                        overlap_msg.append(
                            f"Gap for variable {name} in range {r[0]}:{r[1]}"
                        )

            # Create the final check over the not_covered_values and the covered_numbers
            # Send warning with the combined messages
            logger.log_warning("\n".join(overlap_msg))
            # Only show the first 10 lines. Print all warnings to a txt file.

    def _check_inside_bounds(self, start, end, var):
        return (var > start) & (var < end)

    def _check_new_range(
        self, name, not_covered_values, start_range, end_range, overlap_msg
    ):
        index_range_begin_changed = None
        index_range_end_changed = None
        temp_not_covered_values = not_covered_values.copy()

        for range_ind, not_covered_range in enumerate(not_covered_values):
            start, end = not_covered_range[0], not_covered_range[-1]
            begin_inside = self._check_inside_bounds(start, end, start_range)
            end_inside = self._check_inside_bounds(start, end, end_range)

            # The range is inside the not covered values eg when the user gives the criteria: <=0, >10 and 3:5, making two seperate gaps.
            if begin_inside & end_inside:
                temp_not_covered_values[range_ind] = [start, start_range]
                temp_not_covered_values.insert(range_ind + 1, [end_range, end])
                index_range_begin_changed = range_ind
                index_range_end_changed = range_ind

            # The range starts within the bounds eg when the user gives the criteria: <=0, >10 and 3:15, an overlap and a gap
            elif begin_inside & (not end_inside):

                temp_not_covered_values[range_ind][-1] = start_range
                overlap_msg.append(
                    f"Overlap for variable {name} in range {start_range}:{end}"
                )
                index_range_begin_changed = range_ind

            # The range ends within the bounds eg when the user gives the criteria: <=0, >10 and -3:5, an overlap and a gap
            elif (not begin_inside) & end_inside:
                # temp_not_covered_values[range_ind] = [start, end_range]
                # temp_not_covered_values.insert(range_ind, [end_range, end])
                temp_not_covered_values[range_ind][0] = end_range
                overlap_msg.append(
                    f"Overlap for variable {name} in range {start_range}:{start}"
                )
                index_range_end_changed = range_ind

        # The range is outside the covered values
        if (index_range_begin_changed == None) or (index_range_end_changed == None):
            # eg when the user gives the criteria: <=0, >10 and 13:15, overlap
            if (
                (temp_not_covered_values[-1][-1] < start_range)
                & (temp_not_covered_values[-1][-1] < end_range)
            ) or (
                (start_range < temp_not_covered_values[0][0])
                & (end_range < temp_not_covered_values[0][0])
            ):
                overlap_msg.append(
                    f"Overlap for variable {name} in range {start_range}:{end_range}"
                )

            # The range is larger than the given bounds eg when the user gives the criteria: <=0, >10 and -3:15. All values covered, but overlap
            elif (start_range <= temp_not_covered_values[0][0]) & (
                end_range >= temp_not_covered_values[-1][-1]
            ):
                start_string = f"range {start_range}:{temp_not_covered_values[0][0]}"
                end_string = f"range {temp_not_covered_values[-1][-1]}:{end_range}"
                if start_range == temp_not_covered_values[0][0]:
                    start_string = f"number {start_range}"
                if end_range == temp_not_covered_values[-1][-1]:
                    end = f"number {end_range}"

                overlap_msg.append(
                    f"Overlap for variable {name} in {start_string} and {end_string}"
                )
                temp_not_covered_values = []

            # The start of the range and the end of the range fall in between existing ranges eg <=0, 3:5 >10. New: 2:7 -> overlap message for 3:5. temp_not_covered_values will [[0:3],[5:10]] change to [0:2][7:10]
            else:
                flattened_list = sum(temp_not_covered_values, [])
                print(flattened_list)
                insort(flattened_list, start_range)
                insort(flattened_list, end_range)
                start_insort_index = bisect_right(flattened_list, start_range)
                end_insort_index = bisect_left(flattened_list, end_range)

                if end_insort_index - start_insort_index <= 1:
                    overlap_msg.append(
                        f"Overlap for variable {name} at {start_range}:{end_range}"
                    )
                else:
                    temp_not_covered_values = _np.reshape(
                        flattened_list, (int(len(flattened_list) / 2), 2)
                    )

            # if start == start_range:
            #     overlap_msg.append(
            #         f"Overlap for variable {name} at {start_range}"
            #     )

            # if end == end_range:
            #     overlap_msg.append(
            #         f"Overlap for variable {name} at {end_range}"
            #     )
        return temp_not_covered_values, overlap_msg

    def _make_overlap_message(self, name, start, end, overlap_msg):
        return overlap_msg.append(f"Overlap for variable {name} in range {start}:{end}")
