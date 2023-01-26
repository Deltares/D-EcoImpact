"""
Tests for RuleBase class
"""


from decoimpact.business.entities.rules.i_rule import IRule


def test_create_rule_base_should_set_defaults():
    """Test creating a RuleBase with defaults"""

    # Arrange & Act
    rule = IRule("test")

    # Assert
    assert rule.name == "test"
    assert isinstance(rule, IRule)
