# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
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

from decoimpact.data.api.i_rule_data import IRuleData


class IDepthAverageRuleData(IRuleData, ABC):
    """Data for a DepthAverageRule"""

    @property
    @abstractmethod
    def input_variable(self) -> str:
        """Name of the input variable"""