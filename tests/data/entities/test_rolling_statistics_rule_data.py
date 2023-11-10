# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for RollingStatisticsRuleData class
"""

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.api.time_operation_type import TimeOperationType
from decoimpact.data.entities.rolling_statistics_rule_data import (
    RollingStatisticsRuleData,
)


def test_rulling_statistics_rule_data_creation_logic():
    """The RullingStatisticsRuleData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Act
    data = RollingStatisticsRuleData(
        "test_name", TimeOperationType.MIN, None, "input", "output", "description"
    )

    # Assert

    assert isinstance(data, IRuleData)
    assert data.input_variable == "input"
    assert data.operation == 2
    