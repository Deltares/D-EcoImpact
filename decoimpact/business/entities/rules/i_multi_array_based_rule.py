"""
Module for IMultiArrayBasedRule interface

Interfaces:
    IMultiArrayBasedRule

"""

from abc import ABC, abstractmethod
from typing import List

import xarray as _xr

from decoimpact.business.entities.rules.i_rule import IRule


class IMultiArrayBasedRule(IRule, ABC):
    """Rule applied to an array of values"""

    @abstractmethod
    def execute(self, input_arrays: List[_xr.DataArray]) -> _xr.DataArray:
        """Executes the rule based on the provided dataset"""
