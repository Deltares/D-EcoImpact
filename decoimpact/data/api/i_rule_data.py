"""
Module for IRuleData interface

Interfaces:
    IRuleData

"""

from abc import ABC, abstractmethod
from typing import Any


class IRuleData(ABC):
    """Interface for dataset information"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the rule"""

    @property
    @abstractmethod
    def data(self) -> dict[str, Any]:
        """Read the rule using the name"""
