"""
Module for IRule interface

Interfaces:
    IRule

"""

from abc import ABC, abstractmethod
from typing import List

from decoimpact.crosscutting.i_logger import ILogger


class IRule(ABC):

    """Interface for rules"""

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
    def input_variable_names(self) -> List[str]:
        """Name of the input variable"""

    @property
    @abstractmethod
    def output_variable_name(self) -> List[str]:
        """Name of the output variable"""

    @abstractmethod
    def validate(self, logger: ILogger) -> bool:
        """Validates if the rule is valid

        Returns:
            bool: wether the rule is valid
        """
