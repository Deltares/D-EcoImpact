"""
Tests for validation utilities
"""

from typing import Any, List

import pytest

from decoimpact.data.parsers.validation_utils import (
    validate_all_instances_number,
    validate_start_before_end,
    validate_type_date
)


def test_validate_all_instances_number_correct():
    """Test if all values in a List are numbers"""

    # Arrange
    test_list: List[Any] = [1, 2, 3, 4.0]

    # # Act
    assert validate_all_instances_number(test_list, "test") is None


def test_validate_all_instances_number_incorrect():
    """Validation gives error when not all values in List
    are numbers."""

    # Arrange
    test_list: List[Any] = [1, 2, 3, 4.0, "test"]

    # Act
    with pytest.raises(ValueError) as exc_info:
        validate_all_instances_number(test_list, "test")

    exception_raised = exc_info.value

    # Assert
    assert exception_raised.args[0] == (
        "ERROR in position 4 is type <class 'str'>. "
        "test should be a list of int or floats, received: "
        "[1, 2, 3, 4.0, 'test']"
    )


def test_validate_all_types_dates():
    """Test if all values in a List are dates"""

    # Arrange
    test_list: List[Any] = ["02-03", "12-12"]

    # # Act
    assert validate_type_date(test_list, "test") is None


def test_validate_type_date_with_not_all_strings():
    """Raise a TypeError if an element in the list is
    not a string."""

    # Arrange
    test_list: List[Any] = [1, 2, "test"]

    # Act
    with pytest.raises(TypeError) as exc_info:
        validate_type_date(test_list, "test")

    exception_raised = exc_info.value

    # Assert
    assert exception_raised.args[0] == (
        "test should be a list of strings, received: [1, 2, 'test']. "
        "ERROR in position 0 is type <class 'int'>."
    )


def test_validate_type_date_with_not_all_correct_date_strings():
    """Raise a ValueError if an element in the list is
    not a in the correct date string format DD-MM."""

    # Arrange
    test_list: List[Any] = ["01-01", "12-12-2021"]

    # Act
    with pytest.raises(ValueError) as exc_info:
        validate_type_date(test_list, "test")

    exception_raised = exc_info.value

    # Assert
    assert exception_raised.args[0] == (
        "test should be a list of date strings with Format DD-MM, "
        "received: ['01-01', '12-12-2021']. ERROR in position 1, "
        "string: 12-12-2021."
    )


def test_validate_type_date_with_not_all_correct_date_strings_2():
    """First check if all elements in a list are strings"""

    # Arrange
    test_list: List[Any] = ["10-31"]

    # Act
    with pytest.raises(ValueError) as exc_info:
        validate_type_date(test_list, "test")

    exception_raised = exc_info.value

    # Assert
    assert exception_raised.args[0] == (
        "test should be a list of date strings with Format DD-MM, "
        "received: ['10-31']. ERROR in position 0, string: 10-31."
    )


def test_validate_start_before_end_correct():
    """Test if all elements in the start_date are before end_date"""    # Arrange

    # Arrange
    test_start: List[str] = ["01-01", "10-01"]
    test_end: List[str] = ["11-01", "13-01"]

    # # Act
    assert validate_start_before_end(test_start, test_end) is None


def test_validate_start_before_end_incorrect():
    """Check if all elements in the start_date are before end_date"""    # Arrange

    test_start: List[str] = ["01-01", "10-01"]
    test_end: List[str] = ["02-01", "03-01"]

    # Act
    with pytest.raises(ValueError) as exc_info:
        validate_start_before_end(test_start, test_end)

    exception_raised = exc_info.value

    # Assert
    assert exception_raised.args[0] == (
        "All start dates should be before the end dates. ERROR in "
        "position 1 where start: 10-01 and end: 03-01."
    )
