# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for TimeOperationType

Classes:
    TimeOperationType
"""
from enum import IntEnum


class TimeOperationType(IntEnum):
    """Classify the time operation types."""

    ADD = 1
    MIN = 2
    MAX = 3
    AVERAGE = 4
    MEDIAN = 5
    COUNT_PERIODS = 6
    MAX_DURATION_PERIODS = 7
    AVG_DURATION_PERIODS = 8
    STDEV = 9
    PERCENTILE = 10
