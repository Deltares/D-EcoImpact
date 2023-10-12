# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ICombineResultsRuleData interface

Interfaces:
    ICombineResultsRuleData

"""

from abc import ABC, abstractmethod
from typing import List

from decoimpact.data.api.i_rule_data import IRuleData


class ICombineResultsRuleData(IRuleData, ABC):
    """Data for a combine Results Rule"""

    @property
    @abstractmethod
    def input_variable_names(self) -> List[str]:
        """Name of the input variable"""

    @property
    @abstractmethod
    def operation_type(self) -> str:
        """Property for the operation_type"""

    @property
    @abstractmethod
    def operation_parameter(self) -> float:
        """Property for the operation_parameter"""
