# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for Validation functions
"""

from datetime import datetime
from typing import Any, List


def validate_all_instances_number(data: List, name: str):
    """Check if all instances in a list are of type int or float

    Args:
        data (List): List to check
        name (str): Name to give in the error message

    Raises:
        ValueError: Raise an error to define which value is incorrect
    """
    if not all(isinstance(m, (int, float)) for m in data):
        message = f"{name} should be a list of int or floats, received: {data}"
        position_error = "".join(
            [
                f"ERROR in position {index} is type {type(m)}. "
                for (index, m) in enumerate(data)
                if not isinstance(m, (int, float))
            ]
        )
        raise ValueError(f"{position_error}{message}")


def validate_type_date(data: List[str], name: str):
    """
    Check if all dates in list are a datestring of format: DD-MM

    Args:
        data (str): List of date strings
        name (str): Name of data to address in error message

    Raises:
        ValueError: Raise this error to indicate which value is not
        a date in the proper format.
    """

    for index, date_string in enumerate(data):
        try:
            datetime.strptime(date_string, r"%d-%m")
        except TypeError as exc:
            message = (
                f"{name} should be a list of strings, "
                f"received: {data}. ERROR in position {index} is "
                f"type {type(date_string)}."
            )
            raise TypeError(message) from exc
        except ValueError as exc:
            message = (
                f"{name} should be a list of date strings with Format DD-MM, "
                f"received: {data}. ERROR in position {index}, string: {date_string}."
            )
            raise ValueError(message) from exc


def validate_start_before_end(start_list: List[str], end_list: List[str]):
    """Validate if for each row in the table the start date is before the end date.

    Args:
        start_list (List[str]): list of dates
        end_list (List[str]): list of dates
    """

    for index, (start, end) in enumerate(zip(start_list, end_list)):
        start_str = datetime.strptime(start, r"%d-%m")
        end_str = datetime.strptime(end, r"%d-%m").replace()

        if start_str >= end_str:
            message = (
                f"All start dates should be before the end dates. "
                f"ERROR in position {index} where start: "
                f"{start} and end: {end}."
            )
            raise ValueError(message)


def validate_table_with_input(table, input_variable_names):
    """Check if the headers of the input table and the input variable names match

    Args:
        table (_type_): Table to check the headers from
        input_variable_names (_type_): Variable input names

    Raises:
        ValueError: If there is a mismatch notify the user.
    """
    headers = list(table.keys())
    difference = list(set(headers) - set(input_variable_names))
    if len(difference) != 1:
        raise ValueError(
            f"The headers of the table {headers} and the input "
            f"variables {input_variable_names} should match. "
            f"Mismatch: {difference}"
        )
    if difference[0] != "output":
        raise ValueError("Define an output column with the header 'output'.")


def validate_type(variable: Any, name: str, expected_type: Any):
    """Validation function to check if the variable is of the
    expected type. Otherwise give a ValueError

    Args:
        variable (Any): the variable to check
        name (str): the name of the variable
        type (str): the type the variable should have

    Raises:
        ValueError: If type is not what is should be, raise error
    """
    if not isinstance(variable, expected_type):
        raise ValueError(
            f"The inputfield {name} must be of type {expected_type.__name__}, "
            f"but is of type {type(variable).__name__}"
        )
