# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for dictionary utilities

"""

from typing import Any, Dict, List, Optional, TypeVar

ValueT = TypeVar("ValueT")


def get_dict_element(
    key: str, contents: Dict[str, ValueT], required: bool = True
) -> Optional[ValueT]:
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


def convert_table_element(table: List[Any]) -> Dict[Any, Any]:
    """Convert a table element into a dictionary

    Args:
        table (list[Any]): Table to convert
    Raises:
        ValueError: When table is not correctly defined

    Returns:
        Dict[Any, Any]: readable dictionary with parsed headers and values.
    """

    if len(table) <= 1:
        raise ValueError(
            "Define a correct table with the headers in the first row and values in \
            the others."
        )

    if not all(len(row) == len(table[0]) for row in table):
        raise ValueError("Make sure that all rows in the table have the same length.")

    headers = table[0]

    if len(headers) != len(set(headers)):
        seen = set()
        dupes = [x for x in headers if x in seen or seen.add(x)]
        raise ValueError(
            f"There should only be unique headers. Duplicate values: {dupes}"
        )

    values = list(map(list, zip(*table[1:])))  # transpose list
    return dict(zip(headers, values))
