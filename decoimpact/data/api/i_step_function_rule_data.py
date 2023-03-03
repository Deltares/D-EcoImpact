"""
Module for IStepFunctionRuleData interface

Interfaces:
    IStepFunctionRuleData

"""


from abc import ABC, abstractmethod
from typing import List

from decoimpact.data.api.i_rule_data import IRuleData


class IStepFunctionRuleData(IRuleData, ABC):
    """Data for a step function rule"""

    @property
    @abstractmethod
    def input_variable(self) -> str:
        """Name of the input variable"""

    @property
    @abstractmethod
    def limits(self) -> List[float]:
        """Limits of the intervals defining the step function rule"""

    @property
    @abstractmethod
    def responses(self) -> List[float]:
        """Responses corresponding to each of the intervals
        defining the step function rule"""
