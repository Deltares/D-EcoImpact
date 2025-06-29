# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for RuleBase class
"""

from decoimpact.business.entities.rules.rule_base import RuleBase


class TestRule(RuleBase):
    def validate(self) -> bool:
        return True


def test_create_rule_base_should_set_defaults():
    """Test creating a RuleBase with defaults"""

    # Arrange & Act
    rule = TestRule("test", [])
    # Assert
    assert rule.name == "test"
    assert rule.description == ""
    assert rule.output_variable_name == "output"
    assert isinstance(rule, RuleBase)


def test_setting_name_of_rule():
    """Test setting name of a RuleBase"""

    # Arrange & Act
    rule = TestRule("test", [])

    # Assert
    assert rule.name == "test"
    rule.name = "foo"
    assert rule.name == "foo"


def test_setting_description_of_rule():
    """Test setting description of a RuleBase"""

    # Arrange & Act
    rule = TestRule("test", [])

    # Assert
    assert rule.description == ""
    rule.description = "foo"
    assert rule.description == "foo"


def test_setting_output_variable_name_of_rule():
    """Test setting input_variable_names of a RuleBase"""

    # Arrange & Act
    rule = TestRule("test", [])

    # Assert
    assert rule.output_variable_name == "output"
    rule.output_variable_name = "foo"
    assert rule.output_variable_name == "foo"
