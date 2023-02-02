"""
Module for IArrayBasedRule interface

Interfaces:
    IArrayBasedRule

"""

from abc import ABC, abstractmethod

import xarray as _xr

from decoimpact.business.entities.rules.i_rule import IRule


class IArrayBasedRule(IRule, ABC):
    """Rule applied to an array of values"""

    @abstractmethod
    def execute(self, value_array: _xr.DataArray) -> _xr.DataArray:
        """Executes the rule based on the provided array"""
