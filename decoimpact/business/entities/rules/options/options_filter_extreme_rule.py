# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ExtremeTypeOptions Class

Classes:
    ExtremeTypeOptions
"""
from enum import StrEnum, auto


class ExtremeTypeOptions(StrEnum):
    """Classify the extreme type options."""

    PEAKS = auto()
    TROUGHS = auto()
