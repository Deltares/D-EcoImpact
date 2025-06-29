# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""Module for IResponseCurveRuleData interface

Interfaces:
    IResponseCurveRuleData
"""

from abc import ABC, abstractmethod
from typing import List

from decoimpact.data.api.i_rule_data import IRuleData


class IResponseCurveRuleData(IRuleData, ABC):
    """Data for a response curve rule"""

    @property
    @abstractmethod
    def input_variable(self) -> str:
        """Property for the input variable"""

    @property
    @abstractmethod
    def input_values(self) -> List[float]:
        """Property for the input values"""

    @property
    @abstractmethod
    def output_values(self) -> List[float]:
        """Property for the output values"""
