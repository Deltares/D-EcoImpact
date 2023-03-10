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
