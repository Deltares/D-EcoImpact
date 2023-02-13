"""
Module for IRuleData interface

Interfaces:
    IRuleData

"""

from abc import ABC, abstractmethod


class IRuleData(ABC):
    """Interface for rules data information"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the rule"""

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of the rule"""

    @property
    @abstractmethod
    def output_variable(self) -> str:
        """Read the rule using the name"""
