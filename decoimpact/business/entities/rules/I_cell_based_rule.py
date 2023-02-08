from abc import ABC, abstractmethod

import xarray as _xr

from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.crosscutting.i_logger import ILogger


class ICellBasedRule(IRule, ABC):
    """Rule applied to every cell"""

    @abstractmethod
    def execute(self, value: float, logger: ILogger) -> float:
        """Executes the rule based on the provided value"""
