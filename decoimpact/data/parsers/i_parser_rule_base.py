"""
Module for IParserRuleBase class
Classes:
    IParserRuleBase
"""
from abc import ABC, abstractmethod
from typing import Any, Dict

from decoimpact.business.entities.rules.rule_base import RuleBase


class IParserRuleBase(ABC):
    """Class for the parser of the basic rules"""

    @property
    @abstractmethod
    def rule_type_name(self) -> str:
        """Type name for the rule"""

    @abstractmethod
    def parse_dict(self, dictionary: Dict[str, Any]) -> RuleBase:
        """Parses the provided dictionary to a rule
        Args:
            dictionary (Dict[str, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            RuleBase: Rule based on the provided data
        """
