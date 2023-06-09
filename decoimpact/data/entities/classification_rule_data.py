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

    # TODO: could we remove input_variable_names here?
    @property
    def input_variable_names(self) -> List[str]:
        return self._input_variable_names
