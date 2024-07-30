# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""Module for IFilterExtremesRuleData interface

Interfaces:
    IFilterExtremesRuleData
"""

from abc import ABC, abstractmethod
from typing import List

from decoimpact.data.api.i_rule_data import IRuleData


class IFilterExtremesRuleData(IRuleData, ABC):
    """Data for a filter extremes rule"""

    @property
    @abstractmethod
    def input_variables(self) -> List[str]:
        """List with input variable name"""

    @property
    @abstractmethod
    def extreme_type(self) -> str:
        """Type of extremes [peaks or throughs]"""
