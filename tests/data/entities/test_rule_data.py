# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for RuleData class
"""

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.rule_data import RuleData


def test_rule_data_creation_logic():
    """The RuleData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = RuleData("test_name")
    data.output_variable = "foo"

    # Assert

    assert isinstance(data, IRuleData)
    assert data.name == "test_name"
    assert data.description == ""
    assert data.output_variable == "foo"
