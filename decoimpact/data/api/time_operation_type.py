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
