# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the 
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for IClassificationRuleData interface

Interfaces:
    IClassificationRuleData

"""

from abc import ABC, abstractmethod
from typing import Dict, List

from decoimpact.data.api.i_rule_data import IRuleData


class IClassificationRuleData(IRuleData, ABC):
    """Data for a combine Results Rule"""

    @property
    @abstractmethod
    def input_variable_names(self) -> List[str]:
        """Name of the input variable"""

    @property
    @abstractmethod
    def criteria_table(self) -> Dict[str, List]:
        """Property for the formula"""
