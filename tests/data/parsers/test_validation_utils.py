"""
Tests for validation utilities
"""

from typing import Any, List

import pytest

from decoimpact.data.parsers.validation_utils import validate_all_instances_number


def validate_all_instances_number_correct():
    """Test if all values in a List are numbers"""

    # Arrange
    test_list: List[Any] = [1, 2, 3, 4.0]

    # Act
    with pytest.raises(ValueError) as err:
        validate_all_instances_number(test_list, "test")

    # Assert
    assert str(err.value) == 'Invalid parameter -1'


def validate_all_instances_number_incorrect():
    """Validation gives error when not all values in List
    are numbers."""

    # Arrange
    test_list: List[Any] = [1, 2, 3, 4.0, "test"]

    # Act
    with pytest.raises(ValueError) as exc_info:
        validate_all_instances_number(test_list, "test")

    exception_raised = exc_info.value

    # Assert
    assert exception_raised.args[0] == 'ERROR in position 5 is type <string>.'