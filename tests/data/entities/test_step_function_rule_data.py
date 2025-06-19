# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for the StepFunctionRuleData
"""

from decoimpact.data.entities.step_function_data import StepFunctionRuleData


def test_step_function_rule_data_creation_logic():
    """The StepFunctionRuleData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = StepFunctionRuleData(
        "test_rule_name", [1.0, 2.0, 3.0], [10.0, 20.0, 30.0], "test_input_vars_name"
    )
    data.description = "test_description"
    data.output_variable = "test_output_var_name"

    # Assert

    assert isinstance(data, StepFunctionRuleData)
    assert data.name == "test_rule_name"
    assert data._limits == [1.0, 2.0, 3.0]
    assert data._responses == [10.0, 20.0, 30.0]
    assert data._input_variable == "test_input_vars_name"
    assert data.description == "test_description"
    assert data.output_variable == "test_output_var_name"
