# This file is part of D-EcoImpact
# Copyright (C) 2022-2023  Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the GNU
# Lesser General Public License version 2.1
# A copy of the GNU General Public License can be found at
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

    def __init__(
        self, name: str, output_variable: str = "output", description: str = ""
    ):
        """Create RuleData based on provided info dictionary

        Args:
            info (dict[str, Any]):
        """
        super()
        self._name = name
        self._output_variable = output_variable
        self._description = description

    @property
    def name(self) -> str:
        """Name to the rule"""
        return self._name

    @property
    def description(self) -> str:
        """Description of the rule"""
        return self._description

    @property
    def output_variable(self) -> str:
        """Data of the rule data"""
        return self._output_variable
