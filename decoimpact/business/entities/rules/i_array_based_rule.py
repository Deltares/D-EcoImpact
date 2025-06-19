# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for IArrayBasedRule interface

Interfaces:
    IArrayBasedRule

"""

from abc import ABC, abstractmethod

import xarray as _xr

from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.crosscutting.i_logger import ILogger


class IArrayBasedRule(IRule, ABC):
    """Rule applied to an array of values"""

    @abstractmethod
    def execute(self, value_array: _xr.DataArray, logger: ILogger) -> _xr.DataArray:
        """Executes the rule based on the provided array"""
