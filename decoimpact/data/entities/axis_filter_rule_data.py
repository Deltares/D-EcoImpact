# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for AxisFilterRuleData class

Classes:
    AxisFilterRuleData

"""

from decoimpact.data.api.i_axis_filter_rule_data import IAxisFilterRuleData
from decoimpact.data.entities.rule_data import RuleData


class AxisFilterRuleData(IAxisFilterRuleData, RuleData):
    """Class for storing data related to axis filter rule rule"""

    def __init__(
        self, name: str, element_index: int, axis_name: str, input_variable: str
    ):
        super().__init__(name)
        self._input_variable = input_variable
        self._element_index = element_index
        self._axis_name = axis_name

    @property
    def input_variable(self) -> str:
        """Property for the input variable"""
        return self._input_variable

    @property
    def element_index(self) -> int:
        """Property for the index of the element on the axis to filter on"""
        return self._element_index

    @property
    def axis_name(self) -> str:
        """Property for the dimension name"""
        return self._axis_name
