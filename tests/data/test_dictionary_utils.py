# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for dictionary utilities
"""

from typing import Any, Dict, List

import pytest

from decoimpact.data.dictionary_utils import convert_table_element, get_dict_element


def test_get_dict_element():
    """Test if getting an element of a dictionary works"""

    # Arrange
    test_dict: Dict[str, Any] = {"test": 1, "test2": "abc"}

    # Act
    result1 = get_dict_element("test", test_dict)
    result2 = get_dict_element("test2", test_dict)

    # Assert
    assert result1 == 1
    assert result2 == "abc"


def test_get_dict_element_should_throw_if_required_key_is_missing():
    """Test if an error is thrown if the required key
    is not available in the dictionary"""

    # Arrange
    test_dict: Dict[str, Any] = {"test": 1, "test2": "abc"}

    # Act
    with pytest.raises(AttributeError) as exc_info:
        get_dict_element("test3", test_dict)

    exception_raised = exc_info.value

    # Assert
    assert exception_raised.args[0] == "Missing element test3"


def test_get_dict_element_should_return_none_if_key_is_missing():
    """Test if none is returned when the key is not
    available in the dictionary"""

    # Arrange
    test_dict: Dict[str, Any] = {"test": 1, "test2": "abc"}

    # Act
    result = get_dict_element("test3", test_dict, False)

    # Assert
    assert result is None


def test_get_table_element():
    """Test if converting a table to a dict works"""

    # Arrange
    test_list: List = [["header1", "header2"], ["val1", "val2"], ["val3", "val4"]]

    # Act
    result = convert_table_element(test_list)

    # Assert
    assert result == {"header1": ["val1", "val3"], "header2": ["val2", "val4"]}


def test_table_without_values():
    """Test if incorrect table raises error"""

    # Arrange
    test_list: List = [["header1", "header2"]]

    # Act
    with pytest.raises(ValueError) as exc_info:
        convert_table_element(test_list)

    exception_raised = exc_info.value

    # Assert
    assert (
        exception_raised.args[0]
        == "Define a correct table with the headers in the first row and values in \
            the others."
    )


def test_incorrect_table_shape():
    """Test if incorrect table shape raises an error"""

    # Arrange
    test_list: List = [["header1", "header2", "header1"], ["val1", "val2", "val4"]]

    # Act
    with pytest.raises(ValueError) as exc_info:
        convert_table_element(test_list)

    exception_raised = exc_info.value

    # Assert
    assert (
        exception_raised.args[0]
        == "There should only be unique headers. Duplicate values: ['header1']"
    )


def test_table_lentgh_all_rows():
    """Test if all rows have the same lenght."""

    # Arrange
    test_list: List = [
        ["header1", "header2", "header1"],
        ["val1", "val2", "val4"],
        ["val1", "val2"],
    ]

    # Act
    with pytest.raises(ValueError) as exc_info:
        convert_table_element(test_list)

    exception_raised = exc_info.value

    # Assert
    assert (
        exception_raised.args[0]
        == "Make sure that all rows in the table have the same length."
    )
