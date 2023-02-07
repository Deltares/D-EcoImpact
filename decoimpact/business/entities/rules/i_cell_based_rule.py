"""
Module for ICellBasedRule interface

Interfaces:
    ICellBasedRule

"""

from abc import ABC, abstractmethod
from typing import Any

import xarray as _xr

from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.crosscutting.i_logger import ILogger


class ICellBasedRule(IRule, ABC):
    """Rule applied to every cell"""

    @abstractmethod
    def execute(self, date: Any, value: float, logger: ILogger) -> float:
        """Executes the rule based on the provided value"""

    @abstractmethod
    def after_execute(self, data: _xr.DataArray) -> _xr.DataArray:
        """Action to execute after normal execution has finished"""
