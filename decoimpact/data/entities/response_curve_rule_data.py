"""
Module for ReponseCurveRuleData class

Classes:
    ReponseCurveRuleData

"""

from typing import List

from decoimpact.data.api.i_response_curve_rule_data import IResponseCurveRuleData
from decoimpact.data.entities.rule_data import RuleData


class ResponseCurveRuleData(IResponseCurveRuleData, RuleData):
    """Class for storing data related to multiply rule"""

    def __init__(
        self,
        name: str,
        input_values: List[float],
        output_values: List[float],
        input_variable: str,
        output_variable: str = "output",
        description: str = "",
    ):
        super().__init__(name, output_variable, description)
        self._input_variable = input_variable
        self._input_values = input_values
        self._output_values = output_values

    @property
    def input_variable(self) -> str:
        """Property for the input variable"""
        return self._input_variable

    @property
    def input_values(self) -> List[float]:
        """Property for the input values"""
        return self._input_values

    @property
    def output_values(self) -> List[float]:
        """Property for the output values"""
        return self._output_values
