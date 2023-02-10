"""
Module for MultiplyRuleData class

Classes:
    MultiplyRuleData

"""

from typing import List

from decoimpact.data.api.i_multiply_rule_data import IMultiplyRuleData
from decoimpact.data.entities.rule_data import RuleData


class MultiplyRuleData(IMultiplyRuleData, RuleData):
    """Class for storing data related to multiply rule"""

    def __init__(
        self,
        name: str,
        multipliers: List[float],
        input_variable: str,
        output_variable: str = "output",
        description: str = ""
    ):
        super().__init__(name, output_variable, description)
        self._input_variable = input_variable
        self._multipliers = multipliers

    @property
    def input_variable(self) -> str:
        """Name of the input variable"""
        return self._input_variable

    @property
    def multipliers(self) -> List[float]:
        """Name of the input variable"""
        return self._multipliers
