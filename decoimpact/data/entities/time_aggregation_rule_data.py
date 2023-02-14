"""
Module for TimeAggregationRuleData class

Classes:
    TimeAggregationRuleData

"""

from decoimpact.business.entities.rules.operation_type import OperationType
from decoimpact.data.api.i_time_aggregation_rule_data import ITimeAggregationRuleData
from decoimpact.data.entities.rule_data import RuleData


class TimeAggregationRuleData(ITimeAggregationRuleData, RuleData):
    """Class for storing data related to time_aggregation rule"""

    def __init__(
        self,
        name: str,
        operation: OperationType,
        input_variable: str,
        time_scale: str = "year",
        output_variable: str = "output",
        description: str = "",
    ):
        super().__init__(name, output_variable, description)
        self._input_variable = input_variable
        self._operation = operation
        self._time_scale = time_scale

    @property
    def input_variable(self) -> str:
        """Name of the input variable"""
        return self._input_variable

    @property
    def operation(self) -> OperationType:
        """Operation type"""
        return self._operation

    @property
    def time_scale(self) -> str:
        """time_scale type"""
        return self._time_scale
