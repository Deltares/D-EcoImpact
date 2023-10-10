# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
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


def test_remove_duplicates_from_list():
    """Test if remove_duplicates_from_list returns a list without duplicates"""
    # Arrange
    mylist = ["a", "b", "c", "a", "b", "d", "e"]
    # Act

    myflatlist = utilities.flatten_list(utilities.remove_duplicates_from_list(mylist))
    myflatlist.sort()

    # Assert
    assert myflatlist == ["a", "b", "c", "d", "e"]
