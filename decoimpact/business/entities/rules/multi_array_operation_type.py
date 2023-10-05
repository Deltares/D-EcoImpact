# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the 
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for MultiArrayOperationType Class

Classes:
    MultiArrayOperationType
"""
from enum import IntEnum


class MultiArrayOperationType(IntEnum):
    """Classify the multi array operation types."""

    MULTIPLY = 1
    MIN = 2
    MAX = 3
    AVERAGE = 4
    MEDIAN = 5
    ADD = 6
    SUBTRACT = 7
