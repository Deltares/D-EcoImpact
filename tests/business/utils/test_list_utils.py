"""
Tests for utility functions regarding an xarray dataset
"""

import decoimpact.business.utils.list_utils as utilities


def test_flatten_list_returns_flat_list():
    """Test if flatten_list returns a flat list"""

    # Arrange
    mylist = ["a", "b", ["c"], "d"]

    # Act
    myflatlist = utilities.flatten_list(mylist)

    # Assert
    assert myflatlist == ["a", "b", "c", "d"]

