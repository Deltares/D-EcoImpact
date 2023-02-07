"""
Module for IRuleParser class

Classes:
    IRuleParser
"""
from abc import ABC, abstractmethod
from typing import List

from decoimpact.business.entities.parsers.i_parser_rule_base import IParserRuleBase


class IRuleParsers(ABC):
    """Class for listing all available parsers"""

    @property
    @abstractmethod
    def rule_parsers(self) -> List[IParserRuleBase]:
        """Gives a list of available parsers"""
