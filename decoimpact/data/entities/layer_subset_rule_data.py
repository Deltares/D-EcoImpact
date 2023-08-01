"""
Module for LayerSubsetRuleData class

Classes:
    LayerSubsetRuleData

"""

from decoimpact.data.api.i_layer_subset_rule_data import ILayerSubsetRuleData
from decoimpact.data.entities.rule_data import RuleData


class LayerSubsetRuleData(ILayerSubsetRuleData, RuleData):
    """Class for storing data related to layer subset rule rule"""

    def __init__(
        self,
        name: str,
        start_layer_number: int,
        end_layer_number: int,
        input_variable: str,
        layer_name: str,
        output_variable: str = "output",
        description: str = "",
    ):
        super().__init__(name, output_variable, description)
        self._input_variable = input_variable
        self._start_layer_number = start_layer_number
        self._end_layer_number = end_layer_number
        self._layer_name = layer_name

    @property
    def input_variable(self) -> str:
        """Property for the input variable"""
        return self._input_variable

    @property
    def start_layer_number(self) -> int:
        """Property for the start layer number"""
        return self._start_layer_number

    @property
    def end_layer_number(self) -> int:
        """Property for the end layer number"""
        return self._end_layer_number

    @property
    def layer_name(self) -> str:
        """Property for the layer name"""
        return self._layer_name
