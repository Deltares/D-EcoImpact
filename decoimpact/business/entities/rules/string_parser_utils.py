# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for parser strings
"""


from typing import Any


def str_range_to_list(range_string: str):
    """Convert a string with a range in the form "x:y" of floats to
    two elements (begin and end of range).

    Args:
        range_string (str): String to be converted to a range (begin and end)

    Raises:
        ValueError: If the string is not properly defined

    Returns:
        floats: Return the begin and end value of the range
    """
    range_string = range_string.strip()
    try:
        begin, end = range_string.split(":")
        return float(begin), float(end)
    except ValueError as exc:
        raise ValueError(f'Input "{range_string}" is not a valid range') from exc


def read_str_comparison(compare_str: str, operator: str):
    """Read the string of a comparison (with specified operator) and
    validate if this is in the correct format (<operator><number>, eg: >100)

    Args:
        compare_str (str): String to be checked
        operator (str): Operator to split on

    Raises:
        ValueError: If the compared value is not a number

    Returns:
        float: The number from the comparison string
    """
    compare_str = compare_str.strip()
    try:
        compare_list = compare_str.split(operator)
        if len(compare_list) != 2:
            raise IndexError(
                f'Input "{compare_str}" is not a valid comparison '
                f"with operator: {operator}"
            )
        compare_val = compare_list[1]
        return float(compare_val)
    except ValueError as exc:
        raise ValueError(
            f'Input "{compare_str}" is not a valid comparison with '
            f"operator: {operator}"
        ) from exc


def type_of_classification(class_val: Any) -> str:
    """Determine which type of classification is required: number, range, or
    NA (not applicable)

    Args:
        class_val (_type_): String to classify

    Raises:
        ValueError: Error when the string is not properly defined

    Returns:
        str: Type of classification
    """
    class_type = None
    if isinstance(class_val, (float, int)):
        class_type = "number"
    elif isinstance(class_val, str):
        class_val = class_val.strip()
        if class_val in ("-", ""):
            class_type = "NA"
        elif ":" in class_val:
            str_range_to_list(class_val)
            class_type = "range"
        elif ">=" in class_val:
            read_str_comparison(class_val, ">=")
            class_type = "larger_equal"
        elif "<=" in class_val:
            read_str_comparison(class_val, "<=")
            class_type = "smaller_equal"
        elif ">" in class_val:
            read_str_comparison(class_val, ">")
            class_type = "larger"
        elif "<" in class_val:
            read_str_comparison(class_val, "<")
            class_type = "smaller"

    if not class_type:
        try:
            float(class_val)
            class_type = "number"
        except TypeError as exc:
            raise ValueError(f"No valid criteria is given: {class_val}") from exc

    return class_type
