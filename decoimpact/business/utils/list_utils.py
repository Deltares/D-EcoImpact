"""Library for list utility functions"""


from typing import Any, List


def flatten_list(_2d_list: list[Any]) -> list:
    """Flatten list of lists to one list

    Args:
        _2d_list (list): list to be flattened

    Returns:
        list: flat list
    """
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if isinstance(element, list):
            flat_list = flat_list + [item for item in element]
        else:
            flat_list.append(element)

    return flat_list


def remove_duplicates_from_list(list_with_duplicates: list) -> list:
    """Remove duplicates from list

    Args:
        list (list): list to be made distinct

    Returns:
        list: list without duplicates
    """

    return list(set(list_with_duplicates))


def items_not_in(first: List[str], second: List[str]) -> List[str]:
    """Returns list of items in first list that are not in second list

    Args:
        first (List[str]): list of items to iterate
        second (List[str]): list of items to check

    Returns:
        List[str]: list of items that were not in second list
    """
    return list(filter(lambda var: var not in second, first))


def items_in(first: List[str], second: List[str]) -> List[str]:
    """Returns list of items in first list that are in second list

    Args:
        first (List[str]): list of items to iterate
        second (List[str]): list of items to check

    Returns:
        List[str]: list of items that were in second list
    """
    return list(filter(lambda var: var in second, first))