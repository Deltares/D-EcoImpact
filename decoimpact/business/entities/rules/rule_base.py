"""
Module for RuleBase

Classes:
    RuleBase

"""

from abc import ABC

from decoimpact.business.entities.rules.i_rule import IRule


class RuleBase(IRule, ABC):
    """Implementation of the rule base"""

    def __init__(self, name: str):

        self._name = name
        self._description = ""
        self._output_variable_name = "output"

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
    def output_variable_name(self) -> str:
        """Name of the output variable"""
        return self._output_variable_name

    @output_variable_name.setter
    def output_variable_name(self, output_variable_name: str):
        """Name of the output variable"""
        self._output_variable_name = output_variable_name
