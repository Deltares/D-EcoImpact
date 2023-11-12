# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
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
        self,
        name: str,
        layer_number: int,
        dim_name: str,
        input_variable: str,
        output_variable: str = "output",
        description: str = "",
    ):
        super().__init__(name, output_variable, description)
        self._input_variable = input_variable
        self._layer_number = layer_number
        self._dim_name = dim_name

    @property
    def input_variable(self) -> str:
        """Property for the input variable"""
        return self._input_variable

    @property
    def layer_number(self) -> int:
        """Property for the layer number"""
        return self._layer_number
    
    @property
    def dim_name(self) -> str:
        """Property for the dimension name"""
        return self._dim_name

