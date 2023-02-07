"""
Module for RuletData interface

Classes:
    RuletData

"""

from typing import Any

from decoimpact.data.api.i_rule_data import IRuleData


class RuleData(IRuleData):
    """Class for storing rule information"""

    def __init__(self, rule: dict[str, Any]):
        """Create IRuleData based on provided info dictionary

        Args:
            info (dict[str, Any]):
        """
        super()
        self._name = list(rule.keys())[0]
        self._data = rule[self._name]

    @property
    def name(self) -> str:
        """Name to the rule"""
        return self._name

    @property
    def data(self) -> dict[str, Any]:
        """Data of the rule data"""
        return self._data
