"""
Tests for string parser utilities
"""
import pytest
from decoimpact.business.entities.rules.string_parser_utils import str_range_to_list


def test_str_range_to_list():
    """Test if a range string can be converted to a list"""
    # Arrange
    test_string: str = "100:200"

    # Act
    res1, res2 = str_range_to_list(test_string)

    # Assert
    assert res1 == 100
    assert res2 == 200


def test_str_range_to_list_fails():
    """Test if a range in incorrect format gives an error"""
    # Arrange
    test_string: str = ":100:200"

    # Act
    with pytest.raises(ValueError) as exc_info:
        str_range_to_list(test_string)

    exception_raised = exc_info.value

    # Assert
    assert exception_raised.args[0] == f"Input '{test_string}' is not a valid range"
