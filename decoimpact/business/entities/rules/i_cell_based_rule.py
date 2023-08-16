# This file is part of D-EcoImpact
# Copyright (C) 2022-2023  Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the GNU Lesser General Public
# A copy of the GNU General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ICellBasedRule interface

Interfaces:
    ICellBasedRule

"""

from abc import ABC, abstractmethod

from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.crosscutting.i_logger import ILogger


class ICellBasedRule(IRule, ABC):
    """Rule applied to every cell"""

    @abstractmethod
    def execute(self, value: float, logger: ILogger) -> float:
        """Executes the rule based on the provided value"""
