"""
Module for IMultiArrayBasedRule interface

Interfaces:
    IMultiArrayBasedRule

"""

from abc import ABC, abstractmethod
from typing import Dict

import xarray as _xr

from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.crosscutting.i_logger import ILogger


class IMultiArrayBasedRule(IRule, ABC):
    """Rule applied to an a set of arrays"""

    @abstractmethod
    def execute_single_input(
        self, value_array: _xr.DataArray, logger: ILogger
    ) -> _xr.DataArray:
        """Executes the rule based on the provided dictionary of arrays"""

    @abstractmethod
    def execute_multiple_input(
        self, value_dict: Dict[str, _xr.DataArray], logger: ILogger
    ) -> _xr.DataArray:
        """Executes the rule based on the provided dictionary of arrays"""
