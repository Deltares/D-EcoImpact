"""
Module for ILayerSubsetRuleData interface

Interfaces:
    ILayerSubsetRuleData

"""


from abc import ABC, abstractmethod

from decoimpact.data.api.i_rule_data import IRuleData


class ILayerSubsetRuleData(IRuleData, ABC):
    """Data for a layer subset rule"""

    @property
    @abstractmethod
    def input_variable(self) -> str:
        """Property for the input variable"""

    @property
    @abstractmethod
    def start_layer_number(self) -> int:
        """Property for the start layer number"""

    @property
    @abstractmethod
    def end_layer_number(self) -> int:
        """Property for the end layer number"""

    @property
    @abstractmethod
    def layer_name(self) -> int:
        """Property for the layer name"""
