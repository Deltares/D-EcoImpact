# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for CombineResultsRuleData class

Classes:
    CombineResultsRuleData

"""

from typing import List

from decoimpact.data.api.i_combine_results_rule_data import ICombineResultsRuleData
from decoimpact.data.entities.rule_data import RuleData


class CombineResultsRuleData(ICombineResultsRuleData, RuleData):
    """Class for storing data related to combine results rule"""

    def __init__(
        self,
        name: str,
        input_variable_names: List[str],
        operation_type: str,
        output_variable: str,
        description: str = "",
    ):
        super().__init__(name, output_variable, description)
        self._input_variable_names = input_variable_names
        self._operation_type = operation_type

    @property
    def input_variable_names(self) -> List[str]:
        """Name of the input variable"""
        return self._input_variable_names

    @property
    def operation_type(self) -> str:
        """Name of the input variable"""
        return self._operation_type
