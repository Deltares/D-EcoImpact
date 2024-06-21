# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for (multiple) ClassificationRule class

Classes:
    (multiple) ClassificationRuleData

"""

from decoimpact.data.api.i_depth_average_rule_data import IDepthAverageRuleData
from decoimpact.data.entities.rule_data import RuleData


class DepthAverageRuleData(IDepthAverageRuleData, RuleData):
    """Class for storing data related to formula rule"""

    def __init__(
        self,
        name: str,
        input_variable: str,
    ):
        super().__init__(name)
        self._input_variable = input_variable

    @property
    def input_variable(self) -> str:
        """Name of the input variable"""
        return self._input_variable
