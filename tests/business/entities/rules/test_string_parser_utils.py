# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for string parser utilities
"""
import pytest
from decoimpact.business.entities.rules.string_parser_utils import (
    read_str_comparison,
    str_range_to_list,
    type_of_classification,
)


def test_str_range_to_list():
    """Test function to validate range"""

    # test data
    test_space = "0.5: 5.5"
    test_negative_number = "-3 : 3"

    assert str_range_to_list(test_space) == (0.5, 5.5)
    assert str_range_to_list(test_negative_number) == (-3, 3)


def test_str_range_to_list_fails():
    """Test if a range in incorrect format gives an error"""
    # Arrange
    test_string: str = "0 - 5"

    # Act
    with pytest.raises(ValueError) as exc_info:
        str_range_to_list(test_string)

    exception_raised = exc_info.value

    # Assert
    assert exception_raised.args[0] == f'Input "{test_string}" is not a valid range'


def test_read_str_comparison():
    """Test function to convert str to comparison and return value"""
    assert read_str_comparison(">5", ">") == 5
    assert read_str_comparison("<5", "<") == 5


@pytest.mark.parametrize(
    "test_string, operator",
    [[">=5", ">"], ["5<", "<"], ["<5>", "<"]],
)
def test_read_str_comparison_fails(test_string: str, operator: str):
    """Test if a range in incorrect format gives an error"""
    # Act
    with pytest.raises(ValueError) as exc_info:
        read_str_comparison(test_string, operator)

    exception_raised = exc_info.value

    # Assert
    assert (
        exception_raised.args[0]
        == f'Input "{test_string}" is not a valid comparison with operator: {operator}'
    )


@pytest.mark.parametrize(
    "test_string, operator",
    [
        ["4", "<"],
        ["<<5", "<"],
        ["5<<", "<"],
        ["<5<", "<"],
    ],
)
def test_read_str_comparison_fails_multiple_operators(test_string: str, operator: str):
    """Test if a range in incorrect format gives an error"""
    # Act
    with pytest.raises(IndexError) as exc_info:
        read_str_comparison(test_string, operator)

    exception_raised = exc_info.value

    # Assert
    assert (
        exception_raised.args[0]
        == f'Input "{test_string}" is not a valid comparison with operator: {operator}'
    )


@pytest.mark.parametrize(
    "test_string, result",
    [
        ["12.34", "number"],
        ["-12.34", "number"],
        ["0", "number"],
        ["-", "NA"],
        [">5", "larger"],
        ["<5", "smaller"],
        [">=5", "larger_equal"],
        ["<=5", "smaller_equal"],
        [5, "number"],
        [-8.0, "number"],
    ],
)
def test_type_of_classification(test_string: str, result: str):
    """Test function to type classification"""
    assert type_of_classification(test_string) == result


@pytest.mark.parametrize(
    "test_string",
    [["hello"], [">=5"], ["5<"], [""], ["--"], [":100:199"], ["3:>9"]],
)
def test_type_of_classification_fails(test_string: str):
    """Test function to type classification for failing strings"""
    with pytest.raises(ValueError) as exc_info:
        type_of_classification(test_string)

    exception_raised = exc_info.value
    assert exception_raised.args[0] == f"No valid criteria is given: {test_string}"
