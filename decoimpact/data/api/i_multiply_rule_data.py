# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the 
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for IMultiplyRuleData interface

Interfaces:
    IMultiplyRuleData

"""


from abc import ABC, abstractmethod
from typing import List

from decoimpact.data.api.i_rule_data import IRuleData


class IMultiplyRuleData(IRuleData, ABC):
    """Data for a multiply rule"""

    @property
    @abstractmethod
    def input_variable(self) -> str:
        """Name of the input variable"""

    @property
    @abstractmethod
    def multipliers(self) -> List[List[float]]:
        """Name of the input variable"""

    @property
    @abstractmethod
    def date_range(self) -> List[List[str]]:
        """Array with date ranges"""
