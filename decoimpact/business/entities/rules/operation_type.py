from enum import IntEnum


class OperationType(IntEnum):
    """Classify the operation types."""

    MULTIPLY = (1,)
    MIN = (2,)
    MAX = (3,)
    AVERAGE = (4,)
    MEDIAN = 5
