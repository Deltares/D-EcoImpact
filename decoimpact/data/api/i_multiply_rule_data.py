"""
Module for IMultiplyRuleData interface

Interfaces:
    IMultiplyRuleData

"""


from abc import ABC, abstractmethod
from typing import List

from decoimpact.data.api.i_rule_data import IRuleData


class IMultiplyRuleData(IRuleData, ABC):
    """Data for a multiply rule"""

    @property
    @abstractmethod
    def input_variable(self) -> str:
        """Name of the input variable"""

    @property
    @abstractmethod
    def multipliers(self) -> List[float]:
        """Name of the input variable"""
