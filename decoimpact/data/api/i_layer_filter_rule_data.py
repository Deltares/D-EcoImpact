# This file is part of D-EcoImpact
# Copyright (C) 2022-2023  Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the GNU
# Lesser General Public License version 2.1
# A copy of the GNU General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ILayerFilterRuleData interface

Interfaces:
    ILayerFilterRuleData

"""


from abc import ABC, abstractmethod

from decoimpact.data.api.i_rule_data import IRuleData


class ILayerFilterRuleData(IRuleData, ABC):
    """Data for a layer filter rule"""

    @property
    @abstractmethod
    def input_variable(self) -> str:
        """Property for the input variable"""

    @property
    @abstractmethod
    def layer_number(self) -> int:
        """Property for the layer number"""

    @property
    @abstractmethod
    def layer_name(self) -> int:
        """Property for the layer name"""
