# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for validation logic of the (ClassificationRule) criteria table

"""

from __future__ import annotations

from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

import numpy as _np

from decoimpact.business.entities.rules.string_parser_utils import (
    read_str_comparison,
    str_range_to_list,
    type_of_classification,
)
from decoimpact.crosscutting.i_logger import ILogger


class _Range:
    """Internal class for storing range properties"""

    def __init__(self, start: float, end: float, bnd_name: str = "") -> None:
        self._start: float = start
        self._end: float = end
        self._bnd_name: str = bnd_name

    @property
    def start(self) -> float:
        """Start of the range"""
        return self._start

    @property
    def end(self) -> float:
        """End of the range"""
        return self._end

    @end.setter
    def end(self, end: float):
        self._end = end

    @property
    def bnd_name(self) -> str:
        """Bnd_name of the range"""
        return self._bnd_name

    def check_inside_bounds(self, range_to_compare: _Range) -> Tuple[bool, bool]:
        """Checks if the start and end of provided range (range_to_compare)
        are inside the scope of this range

        Args:
            range_to_compare (_Range): Range to check

        Returns:
            Tuple[bool, bool]: begin inside, end inside
        """
        begin_inside = self._check_inside_bounds(
            range_to_compare.start, range_to_compare.bnd_name
        )
        end_inside = self._check_inside_bounds(
            range_to_compare.end, range_to_compare.bnd_name
        )
        return begin_inside, end_inside

    def _check_inside_bounds(
        self,
        var: float,
        op_cur: Optional[str] = None,
    ) -> bool:
        # Check wether the next value falls within the bounds of the previous range.
        # Some exceptions on > and < defined values.
        if op_cur == "larger":
            left = var > self.start
        else:
            left = var >= self.start

        if self.bnd_name == "smaller":
            right = var < self.end
        else:
            right = var <= self.end
        return left & right

    def __str__(self) -> str:
        return f"({self.start}-{self.end}) {self.bnd_name}"

    def __repr__(self) -> str:
        return str(self)


def validate_table_coverage(crit_table: Dict[str, Any], logger: ILogger):
    """Check if the criteria for the parameters given in the criteria_table
    cover the entire range of data values. If not give the user feedback (warnings)
    concerning gaps and overlaps.

    Args:
        crit_table (Dict[str, Any]): User input describing criteria per parameter
    """
    criteria_table = crit_table.copy()
    del criteria_table["output"]

    new_crit_table = criteria_table.copy()
    unique = True

    # If only 1 parameter is given in the criteria_table check the first parameter
    # on all values and not only the unique values.
    if len(new_crit_table.items()) == 1:
        unique = False

    # Make a loop over all variables from right to left to check combinations
    msgs = []
    for key in reversed(criteria_table.keys()):
        msgs = msgs + list(
            _divide_table_in_unique_chunks(new_crit_table, logger, {}, unique)
        )
        del new_crit_table[key]

    max_msg = 6
    if len(msgs) < max_msg:
        logger.log_warning("\n".join(msgs))
    else:
        # Only show the first 6 lines. Print all msgs to a txt file.
        logger.log_warning("\n".join(msgs[:max_msg]))
        logger.log_warning(
            f"{len(msgs)} warnings found concerning coverage of the "
            f"parameters. Only first {max_msg} warnings are shown. See "
            "multiple_classification_rule_warnings.log file for all warnings."
        )
        with open(
            "multiple_classification_rule_warnings.log", "w", encoding="utf-8"
        ) as file:
            file.write("\n".join(msgs))


def _divide_table_in_unique_chunks(
    criteria_table: Dict[str, Any],
    logger: ILogger,
    conditions: Optional[Dict[str, Any]],
    unique=True,
) -> Iterable[str]:
    """This is a recursive function until all combinations of variables in the
    criteria table is checked on coverage.

    Args:
        criteria_table (Dict[Any,Any]): _description_
        conditions (Optional[Dict[str, Any]]): _description_. Defaults to {}.
        unique (bool, optional): _description_. Defaults to True.
    """
    # This recursive function loops over all variables and filters it on
    # unique values
    if len(criteria_table.items()) != 1:
        crit_to_sort = list(criteria_table.values())[0]
        for unique_c in _np.unique(crit_to_sort):
            indices = [i for i, c in enumerate(crit_to_sort) if c == unique_c]

            # Make a new criteria_table with the remaining variables
            new_crit_table = dict(
                (k, _np.array(v)[indices])
                for i, (k, v) in enumerate(criteria_table.items())
                if i != 0
            )

            key = list(criteria_table.keys())[0]
            if not conditions:
                conditions = {key: unique_c}
            else:
                conditions[key] = unique_c

            # Send the remaining filtered parameters back into the function
            yield from _divide_table_in_unique_chunks(
                new_crit_table, logger, conditions
            )

    else:
        # If there is only one variable, check on all conditions for coverage
        name, criteria = list(criteria_table.items())[0]
        yield from _check_variable_conditions(name, criteria, conditions, unique)


def _check_variable_conditions(
    name: str, criteria: Any, conditions: Optional[Dict[str, Any]], unique: bool
) -> Iterable[str]:
    cond_str = ""

    if conditions and len(conditions) > 0:
        cond_str = ", ".join([f"{key}: {value}" for key, value in conditions.items()])
        # When checking a single parameter or the first parameter
        cond_str = f"For conditions: ({cond_str}). "

    if unique:
        # Little trick to ignore the duplicates when a combination of
        # variables is given. This step is skipped when there is
        # only one parameter given in the criteria_table
        criteria = _np.unique(criteria)

    # WHen there is only one parameter left in the given table ()
    yield from _validate_criteria_on_overlap_and_gaps(name, criteria, cond_str)


def _convert_to_range(val: Any) -> _Range:
    """Make sure all type of accepted criteria is converted to range format
    [start, end]

    Args:
        val: Criteria to be converted (number, range or comparison)

    Returns:
        [start, end]: Returns a range for the criteria given.
                        number -> [val, val]
                        comparison -> [-inf, val] or [val, inf]
                        range -> val
    """

    for bnd_name, operator in [("larger_equal", ">="), ("larger", ">")]:
        if type_of_classification(val) == bnd_name:
            return _Range(read_str_comparison(val, operator), float("inf"), bnd_name)

    for bnd_name, operator in [("smaller_equal", "<="), ("smaller", "<")]:
        if type_of_classification(val) == bnd_name:
            return _Range(float("-inf"), read_str_comparison(val, operator), bnd_name)

    if type_of_classification(val) == "number":
        return _Range(float(val), float(val), "equal")

    if type_of_classification(val) == "range":
        start_range, end_range = str_range_to_list(val)
        return _Range(start_range, end_range, "equal")

    return _Range(float("-inf"), float("inf"))


def _validate_criteria_on_overlap_and_gaps(
    name: str, criteria: Any, pre_warn: str
) -> Iterable[str]:
    """Go over the given criteria to determine if there are gaps or overlaps.

    Args:
        name (str): Name of the parameter
        criteria (Any): The criteria (ranges, numbers of comparisons)
        msgs (List[str]): A list with all gathered warning messages
        pre_warn (str): A prepend message that needs to be included

    Returns:
        List[str]: A list with all gathered warning messages
    """
    # The list of criteria is converted to a list of ranges
    range_criteria = list(map(_convert_to_range, criteria))

    # The ranges needs to be sorted. First on "end" value (1.)
    # then on "start" value (2.)
    # For example: [[1, 4], [0, 5], [-inf, 2] [-inf, 0]]
    # 1. [[-inf, 0], [-inf, 2], [1, 4], [0, 5]]
    # 2. [[-inf, 0], [-inf, 2], [0, 5], [1, 4]]
    sorted_range_criteria = sorted(range_criteria, key=lambda x: x.end)
    sorted_range_criteria = sorted(sorted_range_criteria, key=lambda x: x.start)

    # Check if there are multiple larger or larger and equal comparison values are
    # present, this will cause overlap
    yield from _check_for_multiple_inf_values(name, pre_warn, sorted_range_criteria)

    if len(sorted_range_criteria) > 0 and (
        sorted_range_criteria[0].start != float("-inf")
    ):
        yield _create_warn_message(
            name,
            pre_warn,
            _Range(float("-inf"), sorted_range_criteria[0].start),
            "Gap",
        )

    yield from _check_ranges(name, pre_warn, sorted_range_criteria)

    # Create the final check over the not_covered_values and the covered_numbers
    # Send warning with the combined messages
    if sorted_range_criteria[-1].end != float("inf"):
        yield _create_warn_message(
            name,
            pre_warn,
            _Range(max(list_c.end for list_c in sorted_range_criteria), float("inf")),
            "Gap",
        )


def _check_for_multiple_inf_values(
    name: str, pre_warn: str, sorted_range_criteria: List[_Range]
) -> Iterable[str]:

    def check_start_inf_function(range_to_check: _Range) -> bool:
        return (range_to_check.start == float("-inf")) & (
            range_to_check.end != float("inf")
        )

    def check_end_inf_function(range_to_check: _Range) -> bool:
        return (range_to_check.end == float("inf")) & (
            range_to_check.start != float("-inf")
        )

    checks: List[Tuple[Callable[[_Range], bool], str, bool]] = [
        (check_start_inf_function, "< or <=", True),
        (check_end_inf_function, "> or >=", False),
    ]

    for check_function, operator_str, keep_last in checks:
        multiples = [
            i for i, c in enumerate(sorted_range_criteria) if check_function(c)
        ]

        if keep_last:
            multiples = list(reversed(multiples))

        # remove duplicates for further checking
        for i in multiples[1:]:
            del sorted_range_criteria[i]

        if len(multiples) > 1:
            yield (
                f"{pre_warn}Overlap for variable {name}, multiple criteria with "
                + f"operators {operator_str} are defined."
            )


def _check_ranges(
    name: str, pre_warn: str, sorted_range_criteria: List[_Range]
) -> Iterable[str]:
    for c_ind, crit in enumerate(sorted_range_criteria):
        if c_ind == 0:
            continue

        prev_c = sorted_range_criteria[c_ind - 1]
        begin_inside, end_inside = prev_c.check_inside_bounds(crit)

        # Exception is needed for when a > or < operator is defined. No overlap
        # is defined but also not a gap, so begin_inside and end_inside cover
        # these exceptions properly
        non_equal_overlap = not (
            (("equal" in crit.bnd_name) ^ ("equal" in prev_c.bnd_name))
            & (crit.start == prev_c.end)
        )

        # The range is inside the previous range eg when the user
        # gives the criteria: 0:10 and 3:5, giving one overlap.
        if begin_inside & end_inside:
            yield _create_warn_message(name, pre_warn, crit)
            crit.end = prev_c.end

        # The range starts within the previous range eg when the user
        # gives the criteria: 0:10 and 3:15, an overlap will occur
        elif begin_inside & (not end_inside) & (non_equal_overlap):
            yield _create_warn_message(name, pre_warn, _Range(crit.start, prev_c.end))

        # Because the list is sorted it can never occur that (not
        # "begin_inside) & end_inside" happens

        # The range is completely outside the previous range eg when the user
        # gives the criteria: 0:10 and 15:20, a gap will occur
        elif (not begin_inside) & (not end_inside) & (non_equal_overlap):
            yield _create_warn_message(
                name, pre_warn, _Range(prev_c.end, crit.start), "Gap"
            )


def _create_warn_message(
    name: str,
    pre_warn: str,
    range_used: _Range,
    type_warn: Optional[str] = "Overlap",
) -> str:
    # Create a warning message (default overlap) for given values
    comp_str = f"range {range_used.start}:{range_used.end}"
    if range_used.start == range_used.end:
        comp_str = f"number {range_used.start}"

    return f"{pre_warn}{type_warn} for variable {name} in {comp_str}."
