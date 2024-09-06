# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for (multiple) DepthAverageRule class

Classes:
    (multiple) DepthAverageRuleData

"""

from typing import List

from decoimpact.data.api.i_depth_average_rule_data import IDepthAverageRuleData
from decoimpact.data.entities.rule_data import RuleData


class DepthAverageRuleData(IDepthAverageRuleData, RuleData):
    """Class for storing data related to depth average rule"""

    def __init__(
        self,
        name: str,
        input_variables: List[str],
    ):
        super().__init__(name)
        self._input_variables = input_variables

    @property
    def input_variables(self) -> List[str]:
        """List with input variables"""
        return self._input_variables
