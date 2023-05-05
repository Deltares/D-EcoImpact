"""
Module for IFormulaRuleData interface

Interfaces:
    IFormulaRuleData

"""

from abc import ABC, abstractmethod
from typing import List

from decoimpact.data.api.i_rule_data import IRuleData


class IFormulaRuleData(IRuleData, ABC):
    """Data for a combine Results Rule"""

    @property
    @abstractmethod
    def input_variable_names(self) -> List[str]:
        """Name of the input variable"""

    @property
    @abstractmethod
    def formula(self) -> str:
        """Property for the formula"""
