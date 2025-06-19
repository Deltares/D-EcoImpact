# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for ClassificationRuleData class
"""

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.classification_rule_data import ClassificationRuleData


def test_classification_rule_data_creation_logic():
    """The ClassificationRuleData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Arrange
    test_table = {"a": [1], "output": [2]}

    # Act
    data = ClassificationRuleData("test_name", ["foo", "bar"], test_table)
    data.description = "description"

    # Assert

    assert isinstance(data, IRuleData)
    assert data.criteria_table == test_table
    assert data.input_variable_names == ["foo", "bar"]
