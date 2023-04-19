"""
Module for ICellBasedRule interface

Interfaces:
    ICellBasedRule

"""
from typing import List, Dict
from abc import ABC, abstractmethod

from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.crosscutting.i_logger import ILogger


class ICellBasedRule(IRule, ABC):
    """Rule applied to every cell"""

    @abstractmethod
    def execute_single_input(self, value: float, logger: ILogger) -> float:
        """Executes the rule based on the provided value"""

    @abstractmethod
    def execute_multiple_input(
        self, values: Dict[str, float], logger: ILogger
    ) -> float:
        """Executes the rule based on the provided value"""
