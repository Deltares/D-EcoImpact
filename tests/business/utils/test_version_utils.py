# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for utility functions regarding version number
"""

import re

import decoimpact.business.utils.version_utils as utilities


def test_read_version_number_returns_string_matching_format():
    """Test read_version_number returns a string, corresponding to
    the major.minor.patch form."""

    # Arrange
    # Define the pattern to match the desired format
    pattern = r"^\d+\.\d+\.\d+$"

    # Act
    version_string = utilities.read_version_number()

    # Assert
    assert isinstance(version_string, str)
    assert len(version_string) > 0
    assert re.match(pattern, version_string)
