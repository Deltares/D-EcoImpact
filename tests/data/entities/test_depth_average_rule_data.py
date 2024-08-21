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
    geometry = list(("bedlevel", "waterlevel", "interfacez_z"))
    data = DepthAverageRuleData("test_name",
                                "input1",
                                geometry
                                )

    # Assert

    assert isinstance(data, IRuleData)
    assert data.input_variables == "input1"
    assert data.geometry_variables == geometry
