# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for IAxisFilterRuleData interface

Interfaces:
    IAxisFilterRuleData

"""


from abc import ABC, abstractmethod

from decoimpact.data.api.i_rule_data import IRuleData


class IAxisFilterRuleData(IRuleData, ABC):
    """Data for a axis filter rule"""

    @property
    @abstractmethod
    def input_variable(self) -> str:
        """Property for the nput variable"""

    @property
    @abstractmethod
    def layer_number(self) -> int:
        """Property for the layer number"""
    
    @property
    @abstractmethod
    def dim_name(self) -> str:
        """Property for the dim name"""