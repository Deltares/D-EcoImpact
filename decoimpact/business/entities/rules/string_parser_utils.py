"""
Module for parser strings
"""

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
    except ValueError:
        raise ValueError(f'Input "{range_string}" is not a valid range')


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
        compare_val = compare_str.split(operator)[-1]
        print(compare_val)
        return float(compare_val)
    except ValueError:
        raise ValueError(f'Input "{compare_str}" is not a valid comparison with either > or <')


def type_of_classification(class_val) -> str:
    """Determine which type of classification is required: number, range, or
    NA (not applicable)

    Args:
        class_val (_type_): String to classify

    Raises:
        ValueError: Error when the string is not properly defined

    Returns:
        str: Type of classification
    """

    if type(class_val) == int or type(class_val) == float:
        return "number"
    elif type(class_val) == str:
        class_val = class_val.strip()
        if class_val == "-" or class_val == "":
            return "NA"
        elif ":" in class_val:
            str_range_to_list(class_val)
            return "range"
        elif ">" in class_val:
            read_str_comparison(class_val, ">")
            return "larger"
        elif "<" in class_val:
            read_str_comparison(class_val, "<")
            return "smaller"
        else:
            try:
                float(class_val)
                return "number"
            except ValueError:
                pass

    raise ValueError(f"No valid criteria is given: {class_val}")
