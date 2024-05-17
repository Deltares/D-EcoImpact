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

    def _validate_table_coverage(self, crit_table, logger: ILogger):
        msgs = []
        criteria_table = crit_table.copy()
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
                    cond_str = f"For conditions: ({cond_str}). "
                if unique:
                    # Little trick to ignore the duplicates when a combination of
                    # parameters is given.
                    criteria = _np.unique(criteria)
                self._validate_criteria_on_overlap_and_gaps(
                    name, criteria, msgs, cond_str, logger
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

        if len(msgs) < 10:
            logger.log_warning("\n".join(msgs))
        else:
            logger.log_warning("\n".join(msgs[:10]))
            logger.log_warning(
                f"{len(msgs)} warnings found concerning coverage of the "
                "parameters. Only first 10 msgs are shown. See "
                "classification_warnings.log file for all warnings."
            )
            f = open("classification_warnings.log", "w")
            f.write("\n".join(msgs))
            f.close()
        # Only show the first 10 lines. Print all msgs to a txt file.

    def _convert_to_ranges(self, val):
        # Make sure all type of accepted criteria is converted to range format
        # [start, end]
        for bnd_name, operator in [("larger_equal", ">="), ("larger", ">")]:
            if type_of_classification(val) == bnd_name:
                return [read_str_comparison(val, operator), float("inf"), bnd_name]

        for bnd_name, operator in [("smaller_equal", "<="), ("smaller", "<")]:
            if type_of_classification(val) == bnd_name:
                return [float("-inf"), read_str_comparison(val, operator), bnd_name]

        if type_of_classification(val) == "number":
            return [float(val), float(val), "equal"]

        if type_of_classification(val) == "range":
            start_range, end_range = str_range_to_list(val)
            return [start_range, end_range, "equal"]

    def _validate_criteria_on_overlap_and_gaps(
        self, name, criteria, msgs, pre_warn, logger: ILogger
    ):
        range_criteria = list(map(self._convert_to_ranges, criteria))
        sorted_range_criteria = sorted(range_criteria, key=lambda x: x[1])
        sorted_range_criteria = sorted(sorted_range_criteria, key=lambda x: x[0])

        # Check if there are multiple larger or larger and equal comparison values are
        # present, this will cause overlap
        smaller = [
            i for i, c in enumerate(sorted_range_criteria) if c[0] == float("-inf")
        ]
        if len(smaller) > 1:
            msgs.append(
                f"{pre_warn}Overlap for variable {name}, multiple criteria with "
                "operators < or <= are defined"
            )
        for i in reversed(smaller[:-1]):
            del sorted_range_criteria[i]

        # Check if there are multiple larger or larger and equal comparison values are
        # present, this will cause overlap
        larger = [
            i for i, c in enumerate(sorted_range_criteria) if c[1] == float("inf")
        ]
        if len(larger) > 1:
            msgs.append(
                f"{pre_warn}Overlap for variable {name}, multiple criteria with "
                "operators > or >= are defined"
            )
        for i in larger[1:]:
            del sorted_range_criteria[i]

        for c_ind, crit in enumerate(sorted_range_criteria):
            if c_ind == 0:
                print(crit)
                if crit[0] != float("-inf"):
                    msgs = self._warn_message(
                        name, msgs, pre_warn, float("-inf"), crit[0], "Gap"
                    )

            else:
                prev_c = sorted_range_criteria[c_ind - 1]

                begin_inside = self._check_inside_bounds(
                    prev_c[0], prev_c[1], crit[0], op_prev=prev_c[-1], op_cur=crit[-1]
                )
                end_inside = self._check_inside_bounds(
                    prev_c[0], prev_c[1], crit[1], op_prev=prev_c[-1], op_cur=crit[-1]
                )

                # Exception is needed for when a > or < operator is defined. No overlap
                # is defined but also not a gap, so begin_inside and end_inside cover
                # these exceptions properly
                non_equal_overlap = not (
                    (("equal" in str(crit[-1])) ^ ("equal" in str(prev_c[-1])))
                    & (crit[0] == prev_c[1])
                )

                print(crit, begin_inside, end_inside, non_equal_overlap)
                # The range is inside the previous range eg when the user
                # gives the criteria: 0:10 and 3:5, giving one overlap.
                if begin_inside & end_inside:
                    msgs = self._warn_message(
                        name,
                        msgs,
                        pre_warn,
                        crit[0],
                        crit[1],
                    )
                    crit[1] = prev_c[1]

                # The range starts within the previous range eg when the user gives the # criteria: 0:10 and 3:15, an overlap will occur
                elif begin_inside & (not end_inside) & (non_equal_overlap):
                    msgs = self._warn_message(
                        name,
                        msgs,
                        pre_warn,
                        crit[0],
                        prev_c[1],
                    )

                # Because the list is sorted it can never occur that (not
                # "begin_inside) & end_inside" happens

                # The range is completely outside the previous range eg when the user
                # gives the criteria: 0:10 and 15:20, a gap will occur
                elif (not begin_inside) & (not end_inside) & (non_equal_overlap):
                    msgs = self._warn_message(
                        name, msgs, pre_warn, prev_c[1], crit[0], "Gap"
                    )

        if sorted_range_criteria[-1][1] != float("inf"):
            msgs = self._warn_message(
                name,
                msgs,
                pre_warn,
                max([list_c[1] for list_c in sorted_range_criteria]),
                float("inf"),
                "Gap",
            )

        # Create the final check over the not_covered_values and the covered_numbers
        # Send warning with the combined messages

        return msgs

    def _check_inside_bounds(self, start, end, var, op_prev=None, op_cur=None):
        if op_cur == "larger":
            left = var > start
        else:
            left = var >= start

        if op_prev == "smaller":
            right = var < end
        else:
            right = var <= end

        # return (var > start) & (var < end)
        return left & right

    def _warn_message(self, name, msgs, pre_warn, start, end=None, type_warn="Overlap"):
        comparison_string = f"range {start}:{end}"
        if (start == end) or (end is None):
            comparison_string = f"number {start}"
        msgs.append(f"{pre_warn}{type_warn} for variable {name} in {comparison_string}")
        return msgs
