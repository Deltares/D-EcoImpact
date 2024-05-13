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
from bisect import bisect_left, bisect_right, insort
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
        self._validate_table_coverage(criteria_table, logger)

        output_variable_name = get_dict_element("output_variable", dictionary)
        description = get_dict_element("description", dictionary)

        return ClassificationRuleData(
            name,
            input_variable_names,
            criteria_table,
            output_variable_name,
            description,
        )

    def _validate_table_coverage(self, criteria_table, logger: ILogger):
        overlap_msg = []
        del criteria_table["output"]

        def check_coverage(criteria_table, conditions={}, unique=True):
            # This is a recursive function until all combinations of variables in the
            # criteria table is checked on coverage.
            # If there is only one variable, check on all conditions for coverage
            if len(criteria_table.items()) == 1:
                cond_str = ", ".join(
                    [f"{key}: {value}" for key, value in conditions.items()]
                )
                name, criteria = next(iter(criteria_table.items()))
                if cond_str != "":
                    # When checking a single parameter or the first parameter
                    cond_str = f"For conditions: ({cond_str})."
                if unique:
                    # Little trick to ignore the duplicates when a combination of
                    # parameters is given.
                    criteria = _np.unique(criteria)
                self._validate_criteria_on_overlap_and_gaps(
                    name, criteria, overlap_msg, cond_str, logger
                )
            # Else evaluate the previous variables to get unique combinations back
            else:
                # This recursive function loops over all variables and filters it on
                # unique values
                crit_to_sort = list(criteria_table.values())[0]
                for unique_c in _np.unique(crit_to_sort):
                    indices = [i for i, c in enumerate(crit_to_sort) if c == unique_c]

                    # Make a new criteria_table with the remaining variables
                    new_crit_table = dict(
                        (k, _np.array(v)[indices])
                        for i, (k, v) in enumerate(criteria_table.items())
                        if i != 0
                    )
                    conditions[list(criteria_table.keys())[0]] = unique_c
                    # Send the remaining filtered parameters back into the function
                    check_coverage(new_crit_table, conditions)

        new_crit_table = criteria_table.copy()
        unique = True
        if len(new_crit_table.items()) == 1:
            unique = False
        # Make a loop over all variables from right to left to check combinations
        for key in reversed(criteria_table.keys()):
            check_coverage(new_crit_table, {}, unique)
            del new_crit_table[key]

        if len(overlap_msg) < 10:
            logger.log_warning("\n".join(overlap_msg))
        else:
            logger.log_warning("\n".join(overlap_msg[:10]))
            logger.log_warning(
                f"{len(overlap_msg)} warnings found concerning coverage of the "
                "parameters. Only first 10 warnings are shown. See decoimpact.log "
                "file for all warnings."
            )
        # Only show the first 10 lines. Print all warnings to a txt file.

    def _validate_criteria_on_overlap_and_gaps(
        self, name, criteria, overlap_msg, prepend_msg, logger: ILogger
    ):
        not_covered_values = [-_np.inf, _np.inf]
        covered_numbers = []

        all_criteria = [type_of_classification(val) for val in criteria]
        # Check if there are multiple larger or larger and equal comparison values are
        # present, this will cause overlap
        if all_criteria.count("larger") + all_criteria.count("larger_equal") > 1:
            overlap_msg.append(
                f"{prepend_msg}Overlap for variable {name}, multiple criteria with "
                "operators > or >= are defined"
            )

        # Check if there are multiple larger or larger and equal comparison values are
        # present, this will cause overlap
        if all_criteria.count("smaller") + all_criteria.count("smaller_equal") > 1:
            overlap_msg.append(
                f"{prepend_msg}Overlap for variable {name}, multiple criteria with "
                "operators < or <= are defined"
            )

        # First set the bounds of the criteria range, by checking if there are both >
        # (or >=) and < (or <=) are present. Without these there will always be a gap
        # defined.

        # Check upper bound (> and >=)
        for bnd_name, operator in [("larger_equal", ">="), ("larger", ">")]:
            for val in (c for c in criteria if (type_of_classification(c) == bnd_name)):
                comparison_val = read_str_comparison(val, operator)
                if not_covered_values[-1] > comparison_val:
                    not_covered_values[-1] = comparison_val
                    if bnd_name == "larger_equal":
                        if comparison_val in covered_numbers:
                            overlap_msg = self._warn_message(
                                name, overlap_msg, prepend_msg, comparison_val
                            )
                        else:
                            covered_numbers.append(comparison_val)

        # Check lower bound (< and <=)
        for bnd_name, operator in [("smaller_equal", "<="), ("smaller", "<")]:
            for val in (c for c in criteria if (type_of_classification(c) == bnd_name)):
                comparison_val = read_str_comparison(val, operator)
                if not_covered_values[0] < comparison_val:
                    not_covered_values[0] = comparison_val
                    if bnd_name == "smaller_equal":
                        if comparison_val in covered_numbers:
                            overlap_msg = self._warn_message(
                                name, overlap_msg, prepend_msg, comparison_val
                            )
                        else:
                            covered_numbers.append(comparison_val)

        # If the upperbound is lower than the lower bound there is an overlap
        # For example when the user defines >10 and <100 -> not_covered_values will
        # look like: [100, 10] and there is an overlap between 10 and 100. But all
        # values are covered. So empty not_covered_values array.
        if not_covered_values[0] > not_covered_values[-1]:
            overlap_msg = self._warn_message(
                name,
                overlap_msg,
                prepend_msg,
                not_covered_values[-1],
                not_covered_values[0],
            )
            not_covered_values = []

        # If the upper and lowerbound are the same. And this value is covered in the
        # covered_numbers array: empty the not_covered_values array, all values are
        # covered. For example the user defines >0 and <=0 -> not_covered_values will
        # look like: [0, 0] and the covered_numbers array: [0].
        if len(not_covered_values) != 0:
            if (not_covered_values[0] == not_covered_values[-1]) and (
                not_covered_values[0] in covered_numbers
            ):
                not_covered_values = []

        # If not_covered_values is empty, it means all values are covered. All other
        # defined criteria will cause an overlap.
        if len(not_covered_values) == 0:
            for comparison_string in ["number", "range"]:
                for val in (
                    val
                    for val in criteria
                    if (type_of_classification(val) == comparison_string)
                ):
                    overlap_msg = self._warn_message(
                        name, overlap_msg, prepend_msg, comparison_string, val
                    )

        # If not_covered_values is not empty, the other criteria might fill these gaps.
        # First check on the numbers.
        else:
            new_not_covered_1 = [not_covered_values.copy()]
            for val in (c for c in criteria if (type_of_classification(c) == "number")):
                for range_ind, not_covered_range in enumerate([not_covered_values]):
                    start, end = not_covered_range[0], not_covered_range[-1]
                    # If number is inside the bounds, split up the array into 2 ranges
                    # and add to covered_numbers
                    if self._check_inside_bounds(start, end, float(val)):
                        new_not_covered_1[range_ind] = [start, float(val)]
                        new_not_covered_1.insert(range_ind + 1, [float(val), end])

                    # If the number is the same/ or outside the bound, leave as is and
                    # add to covered_numbers => overlap
                    else:
                        if float(val) not in covered_numbers:
                            covered_numbers.append(float(val))
                        else:
                            overlap_msg = self._warn_message(
                                name, overlap_msg, prepend_msg, float(val)
                            )

            not_covered_values = new_not_covered_1
            for val in (c for c in criteria if type_of_classification(c) == "range"):
                start_range, end_range = str_range_to_list(val)

                not_covered_values, overlap_msg = self._check_new_range(
                    name,
                    not_covered_values,
                    start_range,
                    end_range,
                    overlap_msg,
                    prepend_msg,
                )

        for r in not_covered_values:
            if (r[0] == r[-1]) & (r[0] not in covered_numbers):
                overlap_msg.append(
                    f"{prepend_msg}Gap for variable {name} in number {r[0]}"
                )
            if r[0] != r[-1]:
                overlap_msg.append(
                    f"{prepend_msg}Gap for variable {name} in range {r[0]}:{r[1]}"
                )

        # Create the final check over the not_covered_values and the covered_numbers
        # Send warning with the combined messages

        return overlap_msg

    def _check_inside_bounds(self, start, end, var):
        return (var > start) & (var < end)

    def _check_new_range(
        self, name, not_covered_values, start_range, end_range, overlap_msg, prepend_msg
    ):
        index_range_begin_changed = ""
        index_range_end_changed = ""
        temp_not_covered_values = not_covered_values.copy()

        for range_ind, not_covered_range in enumerate(not_covered_values):
            start, end = not_covered_range[0], not_covered_range[-1]
            begin_inside = self._check_inside_bounds(start, end, start_range)
            end_inside = self._check_inside_bounds(start, end, end_range)

            # The range is inside the not covered values eg when the user gives the
            # criteria: <=0, >10 and 3:5, making two seperate gaps.
            if begin_inside & end_inside:
                temp_not_covered_values[range_ind] = [start, start_range]
                temp_not_covered_values.insert(range_ind + 1, [end_range, end])
                index_range_begin_changed = range_ind
                index_range_end_changed = range_ind

            # The range starts within the bounds eg when the user gives the criteria:
            # <=0, >10 and 3:15, an overlap and a gap
            elif begin_inside & (not end_inside):
                temp_not_covered_values[range_ind][-1] = start_range
                overlap_msg = self._warn_message(
                    name, overlap_msg, prepend_msg, end, end_range
                )
                index_range_begin_changed = range_ind

            # The range ends within the bounds eg when the user gives the criteria:
            # <=0, >10 and -3:5, an overlap and a gap
            elif (not begin_inside) & end_inside:
                temp_not_covered_values[range_ind][0] = end_range
                overlap_msg = self._warn_message(
                    name, overlap_msg, prepend_msg, start_range, start
                )
                index_range_end_changed = range_ind

        # The range is outside the covered values
        if (index_range_begin_changed == "") or (index_range_end_changed == ""):
            # The range is larger than the given bounds eg when the user gives the
            # criteria: <=0, >10 and -3:15. All values covered, but overlap
            if (start_range <= temp_not_covered_values[0][0]) & (
                end_range >= temp_not_covered_values[-1][-1]
            ):
                overlap_msg = self._warn_message(
                    name,
                    overlap_msg,
                    prepend_msg,
                    start_range,
                    temp_not_covered_values[0][0],
                )
                overlap_msg = self._warn_message(
                    name,
                    overlap_msg,
                    prepend_msg,
                    temp_not_covered_values[-1][-1],
                    end_range,
                )

                temp_not_covered_values = []

            else:
                # The start of the range and the end of the range fall in between
                # existing ranges eg <=0, 3:5 >10. New: 2:7 -> overlap message for 3:5.
                # temp_not_covered_values will [[0:3],[5:10]] change to [0:2][7:10]
                flattened_list = sum(temp_not_covered_values, [])
                insort(flattened_list, start_range)
                insort(flattened_list, end_range)
                start_insort_index = bisect_right(flattened_list, start_range)
                end_insort_index = bisect_left(flattened_list, end_range)

                if (end_insort_index - start_insort_index <= 1) and (
                    (index_range_begin_changed == "")
                    and (index_range_end_changed == "")
                ):
                    overlap_msg = self._warn_message(
                        name, overlap_msg, prepend_msg, start_range, end_range
                    )
                elif end_insort_index - start_insort_index > 1:
                    temp_not_covered_values = _np.reshape(
                        flattened_list, (int(len(flattened_list) / 2), 2)
                    )

        return temp_not_covered_values, overlap_msg

    def _warn_message(self, name, overlap_msg, prepend_msg, start, end=None):
        comparison_string = f"range {start}:{end}"
        if (start == end) or (end is None):
            comparison_string = f"number {start}"
        overlap_msg.append(
            f"{prepend_msg}Overlap for variable {name} in {comparison_string}"
        )
        return overlap_msg
