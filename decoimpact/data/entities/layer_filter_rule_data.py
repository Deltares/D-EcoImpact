"""
Module for LayerFilterRuleData class

Classes:
    LayerFilterRuleData

"""

from decoimpact.data.api.i_layer_filter_rule_data import ILayerFilterRuleData
from decoimpact.data.entities.rule_data import RuleData


class LayerFilterRuleData(ILayerFilterRuleData, RuleData):
    """Class for storing data related to layer filter rule rule"""

    def __init__(
        self,
        name: str,
        layer_number: int,
        input_variable: str,
        output_variable: str,
    ):
        super().__init__(name, output_variable)
        self._input_variable = input_variable
        self._layer_number = layer_number

    @property
    def input_variable(self) -> str:
        """Property for the input variable"""
        return self._input_variable

    @property
    def layer_number(self) -> int:
        """Property for the layer number"""
        return self._layer_number
