"""
Module for IMultiArrayBasedRule interface

Interfaces:
    IMultiArrayBasedRule

"""

from abc import ABC, abstractmethod
from typing import List

import xarray as _xr

from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.crosscutting.i_logger import ILogger


class IMultiArrayBasedRule(IRule, ABC):
    """Rule applied to an a set of arrays"""

    @abstractmethod
    def execute(
        self, value_arrays: List[_xr.DataArray], logger: ILogger
    ) -> _xr.DataArray:
        """Executes the rule based on the provided array"""
