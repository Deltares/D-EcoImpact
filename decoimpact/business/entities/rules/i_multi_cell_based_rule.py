"""
Module for IMultiCellBasedRule interface

Interfaces:
    IMultiCellBasedRule

"""

from abc import ABC, abstractmethod
from typing import Dict

from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.crosscutting.i_logger import ILogger


class IMultiCellBasedRule(IRule, ABC):
    """Rule applied to every cell"""

    @abstractmethod
    def execute(self, values: Dict[str, float], logger: ILogger) -> float:
        """Executes the rule based on the provided value"""
