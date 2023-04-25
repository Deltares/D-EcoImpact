"""
Tests for FormulaRuleData class
"""


from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.formula_rule_data import FormulaRuleData


def test_combine_results_rule_data_creation_logic():
    """The FormulaRuleData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = FormulaRuleData(
        "test_name", ["input1", "input2"], "input1 + input2", "output"
    )

    # Assert

    assert isinstance(data, IRuleData)
    assert data.input_variable_names == ["input1", "input2"]
    assert data.formula == "input1 + input2"
