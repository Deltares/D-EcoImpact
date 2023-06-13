"""
Module for Validation functions
"""

from typing import List
from datetime import datetime


def validate_all_instances_number(data: List, name: str):
    """Check if all instances in a list are of type int or float

    Args:
        data (List): List to check
        name (str): Name to give in the error message

    Raises:
        ValueError: Raise an error to define which value is incorrect
    """
    if not all(isinstance(m, (int, float)) for m in data):
        message = (
            f"{name} should be a list of int or floats, "
            f"received: {data}"
        )
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

    for (index, m) in enumerate(data):
        try:
            datetime.strptime(m, r"%d-%m")
        except TypeError:
            message = (
                f"{name} should be a list of strings, "
                f"received: {data}. ERROR in position {index} is type {type(m)}."
            )
            raise TypeError(message)
        except ValueError:
            message = (
                f"{name} should be a list of date strings with Format DD-MM, "
                f"received: {data}. ERROR in position {index}, string: {m}."
            )
            raise ValueError(message)


def validate_start_before_end(start_list: List[str], end_list: List[str]):
    """Validate if for each row in the table the start date is before the end date.

    Args:
        start_list (List[str]): list of dates
        end_list (List[str]): list of dates
    """

    for (index, (start, end)) in enumerate(zip(start_list, end_list)):
        start_str = datetime.strptime(start, r"%d-%m")
        end_str = datetime.strptime(end, r"%d-%m").replace()

        if not start_str < end_str:
            message = (
                f"All start dates should be before the end dates. "
                f"ERROR in position {index} where start: "
                f"{start} and end: {end}."
            )
            raise ValueError(message)
