"""Library for general utility functions"""


def flatten_list(_2d_list: list) -> list:
    """Flatten list of lists to one list

    Args:
        _2d_list (list): list to be flattened

    Returns:
        list
    """
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list


def remove_duplicates_from_list(list_with_duplicates: list) -> list:
    """Remove duplicates from list

    Args:
        list (list): list to be flattened

    Returns:
        list
    """
    my_set = set(frozenset(x) for x in list_with_duplicates)
    list_with_duplicates = [list(x) for x in my_set]
    return list_with_duplicates
