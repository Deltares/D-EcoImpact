"""
Module for dictionary utilities

"""

from typing import Dict, TypeVar

TValue = TypeVar("TValue")


def get_dict_element(
        key: str,
        contents: Dict[str, TValue],
        required: bool = True) -> TValue:

    """Tries to get an element from the provided dictionary

    Args:
        key (str): Name of the element to search for
        contents (Dict[str, Any]): Dictionary to search
        required (bool, optional): If the key needs to be there. Defaults to True.
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
