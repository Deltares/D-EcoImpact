"""
Tests for the ResponseCurveRuleData
"""


from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.response_curve_rule_data import ResponseCurveRuleData


def test_response_curve_rule_data_creation_logic():
    """The ResponseCurveRuleData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = ResponseCurveRuleData(
        "test_name", [1, 2, 3], [3, 2, 0], "input", "output", "description"
    )

    assert isinstance(data, IRuleData)
    assert data.name == "test_name"
    assert data.input_values == [1, 2, 3]
    assert data.output_values == [3, 2, 0]
    assert data.description == "description"
    assert data.output_variable == "output"
