# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
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
        "test_name", "input", [1, 2, 3], [3, 2, 0], "output", "description"
    )

    assert isinstance(data, IRuleData)
    assert data.name == "test_name"
    assert data.input_variable == "input"
    assert data.input_values == [1, 2, 3]
    assert data.output_values == [3, 2, 0]
    assert data.description == "description"
    assert data.output_variable == "output"
