"""
Tests for Classification class
"""


from unittest.mock import Mock

import xarray as _xr

from decoimpact.business.entities.rules.classification_rule import ClassificationRule
from decoimpact.crosscutting.i_logger import ILogger


def test_create_classification_rule_should_set_defaults():
    """Test creating a classification rule with defaults"""

    # test data
    criteria_test_table = {
        "output": [1, 2, 3, 4],
        "water_depth": [.1, 3.33, 5, 5],
        "temperature": ['-', '0.1: 15', 15, '>15'],
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
        "output": [100, 200, 300, 400, 500, 900],
        "water_depth": [11, 12, 13, 13, 15, 0],
        "salinity": ['-', '0.5: 5.5', 8.8, 8.8, 9, 0],
        "temperature": ['-', '-', '-', '-', '>25.0', 0],
    }

    # arrange
    logger = Mock(ILogger)
    rule = ClassificationRule("test", ["water_depth", "salinity"], criteria_test_table)
    test_data = {"water_depth": _xr.DataArray([13, 0, 11, 15, 12]),
        "salinity": _xr.DataArray([8.8, 0, 2, 9, 2.5]),
        "temperature": _xr.DataArray([20, -5, 20, 28, 1])}

    # expected results:
    # 1: take first when multiple apply --> 300
    # 2: no possible classification --> None
    # 3: allow '-' --> 100
    # 4: greater than '>' --> 500
    # 5: range --> 200
    expected_result = _xr.DataArray([300, None, 100, 500, 200])

    # act
    test_result = rule.execute(test_data, logger)

    # assert
    assert _xr.testing.assert_equal(test_result, expected_result) is None

def test_str_range_to_list():
    """test function to validate range"""

    criteria_test_table = {
        "output": [1, 2],
        "water_depth": [3, 4]
    }
    rule = ClassificationRule("test", ["water_depth", "salinity"], criteria_test_table)

    # test data
    test_space = "0.5: 5.5"
    test_colon = "0 - 5"
    test_negative_number = "-3 : 3"

    try:
        result_min, result_max = rule.str_range_to_list(test_colon)
    except ValueError:
        result_min = None
        result_max = None

    assert rule.str_range_to_list(test_space) == (0.5, 5.5)
    assert (result_min, result_max) == (None, None)
    assert rule.str_range_to_list(test_negative_number) == (-3, 3)

def test_type_of_classification():
    "test function to type classification"

    criteria_test_table = {
        "output": [1, 2],
        "water_depth": [3, 4]
    }
    rule = ClassificationRule("test", ["water_depth", "salinity"], criteria_test_table)

    result_text = ''
    try:
        result_text = rule.type_of_classification('hello')
    except ValueError:
        result_text = 'error'

    result_empty_input = ''
    try:
        result_empty_input = rule.type_of_classification(None)
    except ValueError:
        result_empty_input = 'error'

    assert rule.type_of_classification('12.34') == 'number'
    assert rule.type_of_classification('-12.34') == 'number'
    assert rule.type_of_classification('0') == 'number'
    assert rule.type_of_classification('-') == 'NA'
    assert rule.type_of_classification('>5') == 'larger'
    assert rule.type_of_classification('<5') == 'smaller'
    assert result_text == 'error'
    assert result_empty_input == 'error'

