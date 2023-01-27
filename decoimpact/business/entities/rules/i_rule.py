"""
Module for IRule interface

Interfaces:
    IRule

"""

from abc import ABC


class IRule(ABC):
    """Interface for rules"""

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        """Name of the rule"""
        return self._name

    @name.setter
    def name(self, name: str):
        """Name of the rule"""
        self._name = name
