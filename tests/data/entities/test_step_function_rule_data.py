"""
Tests for the StepFunctionRuleData
"""

from decoimpact.data.entities.step_function_data import StepFunctionRuleData


def test_step_function_rule_data_creation_logic():
    """The StepFunctionRuleData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = StepFunctionRuleData(
        "test_rule_name",
        [1.0, 2.0, 3.0],
        [10.0, 20.0, 30.0],
        "test_input_vars_name",
        "test_description",
        "test_output_var_name",
    )

    # Assert

    assert isinstance(data, StepFunctionRuleData)
    assert data.name == "test_rule_name"
    assert data._limits == [1.0, 2.0, 3.0]
    assert data._responses == [10.0, 20.0, 30.0]
    assert data._input_variable == "test_input_vars_name"
    assert data.description == "test_description"
    assert data.output_variable == "test_output_var_name"
