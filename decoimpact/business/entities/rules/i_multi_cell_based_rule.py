# This file is part of D-EcoImpact
# Copyright (C) 2022-2023  Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the GNU Lesser General Public
# A copy of the GNU General Public License can be found at https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for IMultiCellBasedRule interface

Interfaces:
    IMultiCellBasedRule

"""

from abc import ABC, abstractmethod
from typing import Dict

from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.crosscutting.i_logger import ILogger


class IMultiCellBasedRule(IRule, ABC):
    """Rule applied to every cell"""

    @abstractmethod
    def execute(self, values: Dict[str, float], logger: ILogger) -> float:
        """Executes the rule based on the provided value"""
