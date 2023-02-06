"""
Module for RuleBase class

Classes:
    RuleBase

"""
from abc import ABC
from typing import List

from decoimpact.business.entities.rules.periodvalue import PeriodValue


class RuleBase(ABC):

    """Base class for rules"""

    def __init__(
        self,
        name: str,
        input_variable_name: str,
        period_value: List[PeriodValue] = None,
    ):

        self._name = name
        self._description = ""
        self._input_variable_name = input_variable_name
        self._output_variable_name = "output"
        self._period_value = period_value

    @property
    def name(self) -> str:
        """Name of the rule"""
        return self._name

    @name.setter
    def name(self, name: str):
        """Name of the rule"""
        self._name = name

    @property
    def description(self) -> str:
        """Description of the rule"""
        return self._description

    @description.setter
    def description(self, description: str):
        """Description of the rule"""
        self._description = description

    @property
    def input_variable_name(self) -> str:
        """Name of the input variable"""
        return self._input_variable_name

    @input_variable_name.setter
    def input_variable_name(self, input_variable_name: str):
        """Name of the input variable"""
        self._input_variable_name = input_variable_name

    @property
    def output_variable_name(self) -> str:
        """Name of the output variable"""
        return self._output_variable_name

    @output_variable_name.setter
    def output_variable_name(self, output_variable_name: str):
        """Name of the output variable"""
        self._output_variable_name = output_variable_name

    @property
    def period_value(self) -> List[PeriodValue]:
        """periods and values: start_DD_MM, end_DD_MM, value"""
        return self._period_value
