"""
Module for MultiplyRule interface

Classes:
    MultiplyRule
"""

from typing import List

import xarray as _xr

from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule


class MultiplyRule(IArrayBasedRule):
    """Implementation for the multiply rule"""

    def __init__(
        self, name: str, input_variable_names: List[str], multipliers: List[float]
    ):
        super().__init__(name, input_variable_names)
        self._name = name
        self._description = ""
        self._input_variable_names = input_variable_names
        self._output_variable_name = "output"
        self._multipliers = multipliers

    # @property
    # def name(self) -> str:
    #     """Name of the rule"""
    #     return self._name

    # @name.setter
    # def name(self, name: str):
    #     """Name of the rule"""
    #     self._name = name

    # @property
    # def description(self) -> str:
    #     """Description of the rule"""
    #     return self._description

    # @description.setter
    # def description(self, description: str):
    #     """Description of the rule"""
    #     self._description = description

    # @property
    # def input_variable_names(self) -> List[str]:
    #     """Name of the input variable"""
    #     return self._input_variable_names

    # @input_variable_names.setter
    # def input_variable_names(self, input_variable_names: List[str]):
    #     """Name of the input variable"""
    #     self._input_variable_names = input_variable_names

    # @property
    # def output_variable_name(self) -> str:
    #     """Name of the output variable"""
    #     return self._output_variable_name

    # @output_variable_name.setter
    # def output_variable_name(self, output_variable_name: str):
    #     """Name of the output variable"""
    #     self._output_variable_name = output_variable_name

    def execute(self, value_array: _xr.DataArray) -> _xr.DataArray:

        """Multiplies the value with the specified multipliers
        Args:
            value_array (DataArray): values to multiply
        Returns:
            DataArray: Multiplied values
        """

        result_multiplier = 1.0
        for multiplier in self._multipliers:
            result_multiplier = result_multiplier * multiplier

        return _xr.DataArray(value_array * result_multiplier)
