# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for (multiple) ClassificationRule class

Classes:
    (multiple) ClassificationRuleData

"""

from typing import Dict, List

from decoimpact.data.api.i_classification_rule_data import IClassificationRuleData
from decoimpact.data.entities.rule_data import RuleData


class ClassificationRuleData(IClassificationRuleData, RuleData):
    """Class for storing data related to formula rule"""

    def __init__(
        self,
        name: str,
        input_variable_names: List[str],
        criteria_table: Dict[str, List],
        output_variable: str = "output",
        description: str = "",
    ):
        super().__init__(name, output_variable, description)
        self._input_variable_names = input_variable_names
        self._criteria_table = criteria_table

    @property
    def criteria_table(self) -> Dict:
        """Criteria property"""
        return self._criteria_table

    @property
    def input_variable_names(self) -> List[str]:
        return self._input_variable_names
