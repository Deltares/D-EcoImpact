# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Configuration file for hardcoded delft3d variable names
"""

INTERFACES_GENERIC_SUFFIX = "_interface"
INTERFACES_Z_SUFFIX = "_interface_z"
INTERFACES_SIGMA_SUFFIX = "_interface_sigma"
BED_LEVEL_SUFFIX = "_flowelem_bl"
WATER_LEVEL_SUFFIX = "_s1"


delft3d_specific_names = [
    INTERFACES_GENERIC_SUFFIX,
    INTERFACES_Z_SUFFIX,
    INTERFACES_SIGMA_SUFFIX,
    BED_LEVEL_SUFFIX,
    WATER_LEVEL_SUFFIX
    ]
