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

    def __init__(
        self,
        name: str,
        input_variable_names: List[str],
        formula: str,
        output_variable: str,
        description: str = "",
    ):
        super().__init__(name, output_variable, description)
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
