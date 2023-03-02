"""
Module for StepFunctionRuleData class

Classes:
    StepFunctionRuleData

"""

from typing import List

from decoimpact.data.api.i_step_function_rule_data import IStepFunctionRuleData
from decoimpact.data.entities.rule_data import RuleData


class StepFunctionRuleData(IStepFunctionRuleData, RuleData):
    """Class for storing data related to step function rule"""

    def __init__(
        self,
        name: str,
        limits: List[float],
        responses: List[float],
        input_variable: str,
        description: str = "",
        output_variable: str = "output",
    ):
        super().__init__(name, output_variable, description)
        self._input_variable = input_variable
        self._limits = limits
        self._responses = responses

    @property
    def input_variable(self) -> str:
        """Name of the input variable"""
        return self._input_variable

    @property
    def limits(self) -> List[float]:
        """Limits of the interval definition for the step function rule"""
        return self._limits

    @property
    def responses(self) -> List[float]:
        """Step wise responses corresponding to each interval defined by the limits"""
        return self._responses
