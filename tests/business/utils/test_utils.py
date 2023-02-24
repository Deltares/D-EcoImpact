"""
Tests for utility functions regarding an xarray dataset
"""

import decoimpact.business.utils.utils as utilities


def test_flatten_list_returns_flat_list():
    """Test if flatten_list returns a flat list"""

    # Arrange
    mylist = ["a", "b", ["c"], "d"]

    # Act
    myflatlist = utilities.flatten_list(mylist)

    # Assert
    assert myflatlist == ["a", "b", "c", "d"]


# def test_remove_duplicates_from_List():
#     """Test if remove_duplicates_from_list returns a list without duplicates"""

#     # Arrange
#     mylist = ["a", "b", "c", "a", "b", "d", "e"]

#     # Act
#     myflatlist = utilities.flatten_list(
#         utilities.remove_duplicates_from_list(mylist)
#     ).sort()

#     # Assert
#     assert myflatlist == ["a", "b", "c", "d", "e"]
