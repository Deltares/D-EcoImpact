# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for FormulaRuleData class

Classes:
    FormulaRuleData

"""

from typing import List

from decoimpact.data.api.i_formula_rule_data import IFormulaRuleData
from decoimpact.data.entities.rule_data import RuleData


class FormulaRuleData(IFormulaRuleData, RuleData):
    """Class for storing data related to formula rule"""

    def __init__(self, name: str, input_variable_names: List[str], formula: str):
        super().__init__(name)
        self._input_variable_names = input_variable_names
        self._formula = formula

    @property
    def input_variable_names(self) -> List[str]:
        """List of input variable names"""
        return self._input_variable_names

    @property
    def formula(self) -> str:
        """Formula as string using input variable names"""
        return self._formula
