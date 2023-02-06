"""
Module for PeriodValue class

Classes:
    PeriodValue

"""


# class PeriodValue(startDDMM: str, endDDMM: str, value: float):
class PeriodValue:

    """Class for type period_value inside rule"""

    def __init__(self, startDDMM: str, endDDMM: str, value: float):
        self._startDDMM = startDDMM
        self._endDDMM = endDDMM
        self._value = value

    @property
    def startDDMM(self) -> str:
        """start day and month of the period"""
        return self._startDDMM

    @property
    def endDDMM(self) -> str:
        """end day and month of the period"""
        return self._endDDMM

    @property
    def value(self) -> float:
        """value for the given period"""
        return self._value
