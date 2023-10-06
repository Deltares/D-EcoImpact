# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the 
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for MultiplyRuleData class

Classes:
    MultiplyRuleData

"""

from typing import List

from decoimpact.data.api.i_multiply_rule_data import IMultiplyRuleData
from decoimpact.data.entities.rule_data import RuleData


class MultiplyRuleData(IMultiplyRuleData, RuleData):
    """Class for storing data related to multiply rule"""

    def __init__(
        self,
        name: str,
        multipliers: List[List[float]],
        input_variable: str,
        output_variable: str = "output",
        description: str = "",
        date_range: List[List[str]] = [],
    ):
        super().__init__(name, output_variable, description)
        self._input_variable = input_variable
        self._multipliers = multipliers
        self._date_range = date_range

    @property
    def input_variable(self) -> str:
        """Name of the input variable"""
        return self._input_variable

    @property
    def multipliers(self) -> List[List[float]]:
        """List of list with the multipliers"""
        return self._multipliers

    @property
    def date_range(self) -> List[List[str]]:
        """List of list with start and end dates"""
        return self._date_range
