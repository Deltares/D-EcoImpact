from abc import ABC, abstractmethod

import xarray as _xr

from decoimpact.business.entities.rules.rule_base import RuleBase


class CellBasedRule(RuleBase, ABC):
    """Rule applied to every cell"""

    @abstractmethod
    def execute(self, data, value: float) -> float:
        """Executes the rule based on the provided value"""
        pass

    def after_execute(self, data: _xr.DataArray) -> _xr.DataArray:
        """Action to execute after normal execution has finished"""
        pass
