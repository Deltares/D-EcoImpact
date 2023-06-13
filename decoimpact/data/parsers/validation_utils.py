"""
Module for Validation functions
"""

from typing import List


def validate_all_instances_number(data: List, name: str):
    """Check if all instances in a list are of type int of float

    Args:
        data (List): List to check
        name (str): Name to give in the error message

    Raises:
        ValueError: Raise an error to feine which value is incorrect
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

    Args:
        data (str): List of date strings
        name (str): Name of data to address in error message

    Raises:
        ValueError: Raise this error to indicate which value is not a date
    """
    if not all(isinstance(m, (str)) for m in data):
        message = (
            f"{name} should be a list of date strings, "
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
        
