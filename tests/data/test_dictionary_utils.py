"""
Tests for dictionary utilities
"""

from typing import Any, Dict

import pytest

from decoimpact.data.dictionary_utils import get_dict_element


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
