# This file is part of D-EcoImpact
# Copyright (C) 2022-2023  Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the GNU
# Lesser General Public License version 2.1
# A copy of the GNU General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
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
    """Rule applied to an a set of (named) arrays"""

    @abstractmethod
    def execute(
        self, value_arrays: Dict[str, _xr.DataArray], logger: ILogger
    ) -> _xr.DataArray:
        """Executes the rule based on the provided array"""
