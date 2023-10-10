# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for FormulaRuleData class
"""


from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.formula_rule_data import FormulaRuleData


def test_formula_rule_data_creation_logic():
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
