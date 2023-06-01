"""
Module for dictionary utilities

"""

from typing import Dict, List, Optional, TypeVar

import pandas as pd

TValue = TypeVar("TValue")


def get_dict_element(
    key: str, contents: Dict[str, TValue], required: bool = True
) -> Optional[TValue]:
    """Tries to get an element from the provided dictionary.

    Args:
        key (str): Name of the element to search for
        contents (Dict[str, Any]): Dictionary to search
        required (bool, optional): If the key needs to be there. Defaults
        to True.
    Raises:
        AttributeError: Thrown when the key is required but is missing).

    Returns:
        T: Value for the specified key
    """
    has_element = key in contents.keys()

    if has_element:
        return contents[key]

    if required:
        raise AttributeError(f"Missing element {key}")

    return None


def convert_table_element(table: List) -> Dict:
    """Convert a table element into a dictionary

    Args:
        table (list): Table to convert
    Raises:
        ValueError: When table is not correctly defined

    Returns:
        Dict: readable dictionary with parsed headers and values.
    """

    print(len)

    if len(table) <= 1:
        raise ValueError(
            "Define a correct table with the headers in the first row and values in \
            the others."
        )

    headers = table[0]
    values = list(map(list, zip(*table[1:])))  # transpose list
    return dict(zip(headers, values))
