# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for FilterExtremesRuleData class
"""


from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.filter_extremes_rule_data import FilterExtremesRuleData


def test_filter_extremes_rule_data_creation_logic():
    """The FilterExtremesRuleData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = FilterExtremesRuleData("test_name", "input1", "peaks", 1, "hour", True)

    # Assert
    assert isinstance(data, IRuleData)
    assert data.input_variables == "input1"
    assert data.distance == 1
    assert data.mask == True
    assert data.time_scale == "hour"
