"""
Module for ILayerFilterRuleData interface

Interfaces:
    ILayerFilterRuleData

"""


from abc import ABC, abstractmethod

from decoimpact.data.api.i_rule_data import IRuleData


class ILayerFilterRuleData(IRuleData, ABC):
    """Data for a layer filter rule"""

    @property
    @abstractmethod
    def input_variable(self) -> str:
        """Property for the nput variable"""

    @property
    @abstractmethod
    def layer_number(self) -> int:
        """Property for the layer number"""
