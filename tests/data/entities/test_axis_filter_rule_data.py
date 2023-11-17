# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for AxisFilterRuleData class
"""

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.axis_filter_rule_data import AxisFilterRuleData


def test_axis_filter_rule_data_creation_logic():
    """The AxisFilterRuleData should parse the provided dictionary
    to correctly initialize itself during creation """
    
    #Act
    data = AxisFilterRuleData("test_name", 3, "dim_name", "input", "output", "description")
    
    
    #Assert
    
    assert isinstance(data, IRuleData)
    assert data.input_variable == "input"
    assert data.layer_number == 3
    assert data.dim_name == "dim_name"