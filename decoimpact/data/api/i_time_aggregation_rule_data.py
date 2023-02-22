"""
Module for ITimeAggregationRuleData interface

Interfaces:
    ITimeAggregationRuleData

"""


from abc import ABC, abstractmethod

from decoimpact.business.entities.rules.time_operation_type import TimeOperationType
from decoimpact.data.api.i_rule_data import IRuleData


class ITimeAggregationRuleData(IRuleData, ABC):
    """Data for a TimeAggregationRule"""

    @property
    @abstractmethod
    def input_variable(self) -> str:
        """Name of the input variable"""

    @property
    @abstractmethod
    def operation(self) -> TimeOperationType:
        """Operation type"""

    @property
    @abstractmethod
    def time_scale(self) -> str:
        """Time scale"""
