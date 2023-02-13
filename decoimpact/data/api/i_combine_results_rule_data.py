"""
Module for ICombineResultsRuleData interface

Interfaces:
    ICombineResultsRuleData

"""

from abc import ABC, abstractmethod
from typing import List

from decoimpact.data.api.i_rule_data import IRuleData


class ICombineResultsRuleData(IRuleData, ABC):
    """Data for a combine Results Rule"""

    @property
    @abstractmethod
    def input_variable_names(self) -> List[str]:
        """Name of the input variable"""

    @property
    @abstractmethod
    def operation_type(self) -> str:
        """Name of the input variable"""
