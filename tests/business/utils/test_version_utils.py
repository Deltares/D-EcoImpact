# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for utility functions regarding version number
"""

import decoimpact.business.utils.version_utils as utilities
import re

def test_flatten_list_returns_flat_list():
    """Test read_version_number returns a string, corresponding to
    the major.minor.patch form."""

# Arramge
# Define the pattern to match the desired format
pattern = r'^\d+\.\d+\.\d+$'
    # Act
    version_string = utilities.read_version_number()

    # Assert
    assert isinstance(version_string, str)
    assert len(version_string) > 0
    
    re.match(pattern, input_string):
