"""
Module for dictionary utilities

"""

from typing import Dict, List, Optional, TypeVar

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

    if len(table) <= 1:
        raise ValueError(
            "Define a correct table with the headers in the first row and values in \
            the others."
        )

    if not all(len(row) == len(table[0]) for row in table):
        raise ValueError('Make sure that all rows in the table have the same length.')

    headers = table[0]

    if len(headers) != len(set(headers)):
        seen = set()
        dupes = [x for x in headers if x in seen or seen.add(x)]
        raise ValueError(
            f"There should only be unique headers. Duplicate values: {dupes}"
        )

    values = list(map(list, zip(*table[1:])))  # transpose list
    return dict(zip(headers, values))
