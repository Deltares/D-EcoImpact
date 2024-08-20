# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for DepthAverageRuleData class
"""


from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.depth_average_rule_data import DepthAverageRuleData


def test_depth_average_rule_data_creation_logic():
    """The DepthAverageRuleData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = DepthAverageRuleData("test_name",
                                "input1",
                                "bedlevel",
                                "waterlevel",
                                "interfaces_z"
                                )

    # Assert

    assert isinstance(data, IRuleData)
    assert data.input_variables == "input1"
    assert data.bed_level_variable == "bedlevel"
    assert data.water_level_variable == "waterlevel"
    assert data.interfaces_variable == "interfaces_z"
