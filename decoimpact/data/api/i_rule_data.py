# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for IRuleData interface

Interfaces:
    IRuleData

"""

from abc import ABC, abstractmethod


class IRuleData(ABC):
    """Interface for rules data information"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the rule"""

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of the rule"""

    @property
    @abstractmethod
    def output_variable(self) -> str:
        """Read the rule using the name"""
