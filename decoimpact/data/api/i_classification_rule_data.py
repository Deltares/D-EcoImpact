"""
Module for IClassificationRuleData interface

Interfaces:
    IClassificationRuleData

"""

from abc import ABC, abstractmethod
from typing import Dict, List

from decoimpact.data.api.i_rule_data import IRuleData


class IClassificationRuleData(IRuleData, ABC):
    """Data for a combine Results Rule"""

    @property
    @abstractmethod
    def input_variable_names(self) -> List[str]:
        """Name of the input variable"""

    @property
    @abstractmethod
    def criteria_table(self) -> Dict[str, List]:
        """Property for the formula"""
