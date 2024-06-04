# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for LayerFilterRuleData class
"""

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.layer_filter_rule_data import LayerFilterRuleData


def test_layer_filter_rule_data_creation_logic():
    """The LayerFilterRuleData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = LayerFilterRuleData("test_name", 3, "input")

    # Assert

    assert isinstance(data, IRuleData)
    assert data.input_variable == "input"
    assert data.layer_number == 3
