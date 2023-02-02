"""
Tests for RuleBase class
"""


from decoimpact.business.entities.rules.i_rule import IRule


def test_create_rule_base_should_set_defaults():
    """Test creating a RuleBase with defaults"""

    # Arrange & Act
    rule = IRule("test", ["foo"])
    # Assert
    assert rule.name == "test"
    assert rule.description == ""
    assert rule._input_variable_names == ["foo"]
    assert rule._output_variable_name == "output"
    assert isinstance(rule, IRule)


def test_setting_name_of_rule():
    """Test setting name of a RuleBase"""

    # Arrange & Act
    rule = IRule("test", ["foo"])

    # Assert
    assert rule.name == "test"
    rule.name = "foo"
    assert rule.name == "foo"


def test_setting_description_of_rule():
    """Test setting description of a RuleBase"""

    # Arrange & Act
    rule = IRule("test", ["foo"])

    # Assert
    assert rule.description == ""
    rule.description = "foo"
    assert rule.description == "foo"


def test_setting_input_variable_names_of_rule():
    """Test setting input_variable_names of a RuleBase"""

    # Arrange & Act
    rule = IRule("test", ["foo"])

    # Assert
    assert rule.input_variable_names == ["foo"]
    rule.input_variable_names = ["foo", "bar"]
    assert rule.input_variable_names == ["foo", "bar"]


def test_setting_output_variable_name_of_rule():
    """Test setting input_variable_names of a RuleBase"""

    # Arrange & Act
    rule = IRule("test", ["foo"])

    # Assert
    assert rule.output_variable_name == "output"
    rule.output_variable_name = "foo"
    assert rule.output_variable_name == "foo"
