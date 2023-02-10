"""
Module for RuleData interface

Classes:
    RuleData

"""


from decoimpact.data.api.i_rule_data import IRuleData


class RuleData(IRuleData):
    """Class for storing rule information"""

    def __init__(self, name: str, output_variable: str):
        """Create RuleData based on provided info dictionary

        Args:
            info (dict[str, Any]):
        """
        super()
        self._name = name
        self._output_variable = output_variable

    @property
    def name(self) -> str:
        """Name to the rule"""
        return self._name

    @property
    def output_variable(self) -> str:
        """Data of the rule data"""
        return self._output_variable
