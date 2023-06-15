"""
Tests for Classification class
"""


from unittest.mock import Mock

from decoimpact.business.entities.rules.classification_rule import ClassificationRule
from decoimpact.crosscutting.i_logger import ILogger

# TODO: add test for multiple possible results (/rules)
# TODO: add test for dummy value "-" in criteria table


def test_create_classification_rule_should_set_defaults():
    """Test creating a classification rule with defaults"""

    # test data
    criteria_test_table = {
        "output": [100, 200, 300, 400, 500],
        "water_depth": [11, 12, 13, 14, 15],
        "salinity": [6, 7, 8, 9, 10]
    }

    # Arrange and act
    rule = ClassificationRule("test", ["water_depth", "salinity"], criteria_test_table)

    # assert
    assert rule.name == "test"
    assert rule.input_variable_names == ["water_depth", "salinity"]
    assert rule.criteria_table == criteria_test_table
    assert rule.output_variable_name == "output"
    assert rule.description == ""
    assert isinstance(rule, ClassificationRule)


def test_execute_classification():
    """Test executing a classification of values"""

    # test data
    criteria_test_table = {
        "output": [100, 200, 300, 400, 500],
        "water_depth": [11.1, 12, 13, 14, 15],
        "salinity": [6.0, 7, 8, 9, 10]
    }

    # arrange
    logger = Mock(ILogger)
    rule = ClassificationRule("test", ["water_depth", "salinity"], criteria_test_table)
    test_data = {'water_depth': 11.1, 'salinity': 6.0}

    # act
    result = rule.execute(test_data, logger)

    # assert
    assert result == 100

