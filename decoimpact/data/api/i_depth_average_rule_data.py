# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for IDepthAverageRuleData interface

Interfaces:
    IDepthAverageRuleData

"""


from abc import ABC, abstractmethod
from typing import List

from decoimpact.data.api.i_rule_data import IRuleData


class IDepthAverageRuleData(IRuleData, ABC):
    """Data for a DepthAverageRule"""

    @property
    @abstractmethod
    def input_variables(self) -> List[str]:
        """List with input variable name, bed level name,
        water level name and interface name (z or sigma)"""
