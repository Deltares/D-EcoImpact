"""
Tests for RuleBase class
"""


from decoimpact.business.entities.rules.rule_base import RuleBase


def test_create_rule_base_should_set_defaults():
    """Test creating a RuleBase with defaults"""

    # Arrange & Act
    rule = RuleBase("test")

    # Assert
    assert rule.name == "test"
    assert isinstance(rule, RuleBase)
