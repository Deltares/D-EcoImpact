# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for RuleData interface

Classes:
    RuleData

"""


from abc import ABC

from decoimpact.data.api.i_rule_data import IRuleData


class RuleData(IRuleData, ABC):
    """Class for storing rule information"""

    def __init__(self, name: str):
        """Create RuleData based on provided info dictionary

        Args:
            info (dict[str, Any]):
        """
        super()
        self._name = name
        self._output_variable = "output"
        self._description = ""

    @property
    def name(self) -> str:
        """Name to the rule"""
        return self._name

    @property
    def description(self) -> str:
        """Description of the rule"""
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def output_variable(self) -> str:
        """Name of the output variable of the rule"""
        return self._output_variable

    @output_variable.setter
    def output_variable(self, output_variable: str):
        self._output_variable = output_variable
