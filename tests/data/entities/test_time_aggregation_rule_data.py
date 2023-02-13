"""
Tests for TimeAggregationRuleData class
"""

from decoimpact.business.entities.rules.operation_type import OperationType
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.time_aggregation_rule_data import TimeAggregationRuleData


def test_time_aggregation_rule_data_creation_logic():
    """The TimeAggregationRuleData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = TimeAggregationRuleData("test_name", OperationType.MIN, "input", "output", "description")

    # Assert

    assert isinstance(data, IRuleData)
    assert data.input_variable == "input"
    assert data.operation == 2
