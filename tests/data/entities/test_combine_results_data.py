"""
Tests for CombineResultsRuleData class
"""


from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.combine_results_rule_data import CombineResultsRuleData


def test_combine_results_rule_data_creation_logic():
    """The CombineResultsRuleData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = CombineResultsRuleData(
        "test_name", ["input1", "input2"], "MULTIPLY", "output"
    )

    # Assert

    assert isinstance(data, IRuleData)
    assert data.input_variable_names == ["input1", "input2"]
    assert data.operation_type == "MULTIPLY"