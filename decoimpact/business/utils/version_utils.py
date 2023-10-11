# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for version utils
"""
from importlib.metadata import version


def read_version_number():
    """Reads the version of the tool

    Returns:
        str: version number of tool
    """
    version_string = version("decoimpact")
    return version_string
