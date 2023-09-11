# This file is part of D-EcoImpact
# Copyright (C) 2022-2023  Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the GNU
# Lesser General Public License version 2.1
# A copy of the GNU General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for MultiplyRuleData class
"""

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.multiply_rule_data import MultiplyRuleData


def test_multiply_rule_data_creation_logic():
    """The MultiplyRuleData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = MultiplyRuleData("test_name", [1.0, 2.0], "input", "output", "description")

    # Assert

    assert isinstance(data, IRuleData)
    assert data.input_variable == "input"
    assert data.multipliers == [1.0, 2.0]
