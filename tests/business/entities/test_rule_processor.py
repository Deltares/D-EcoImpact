"""
Tests for RuleBasedModel class
"""


from typing import List
from unittest.mock import Mock

import numpy as _np
import pytest
import xarray as _xr
from mock import ANY

from decoimpact.business.entities.rule_processor import RuleProcessor
from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.i_cell_based_rule import ICellBasedRule
from decoimpact.business.entities.rules.i_multi_array_based_rule import (
    IMultiArrayBasedRule,
)
from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.crosscutting.i_logger import ILogger


def _create_test_rules() -> List[IRule]:
    """
           +------+
    test --|  R1  |-- out1 --+
           +------+          |  +-----+
                             +--|     |
                                |  R3 |-- out3 --+
                             +--|     |          |
           +------+          |  +-----+          |
    test --|  R2  |-- out2 --+                   |
           +------+                              |  +-----+
                                                 +--|     |
                                                    |  R4 |-- out4
    test -------------------------------------------|     |
                                                    +-----+
    """
    rule1 = Mock(IRule, id="rule1")
    rule2 = Mock(IRule, id="rule2")
    rule3 = Mock(IRule, id="rule3")
    rule4 = Mock(IRule, id="rule4")

    type(rule1).input_variable_names = ["test"]
    type(rule2).input_variable_names = ["test"]
    type(rule3).input_variable_names = ["out1", "out2"]
    type(rule4).input_variable_names = ["out3", "test"]

    type(rule1).output_variable_name = "out1"
    type(rule2).output_variable_name = "out2"
    type(rule3).output_variable_name = "out3"
    type(rule4).output_variable_name = "out4"

    return [rule1, rule2, rule3, rule4]


def test_creating_rule_processor_without_rules_should_throw_exception():
    """Test if rules are correctly checked during creation of the processor"""

    # Arrange
    dataset = _xr.Dataset()
    dataset["test"] = _xr.DataArray([32, 94, 9])

    rules = []

    # Act
    with pytest.raises(ValueError) as exc_info:
        RuleProcessor(rules, [dataset])

    exception_raised = exc_info.value

    # Assert
    expected_message = "No rules defined."
    assert exception_raised.args[0] == expected_message


def test_creating_rule_processor_without_input_datasets_should_throw_exception():
    """Test if input datasets are correctly checked during creation of the processor"""

    # Arrange
    rule = Mock(IRule)

    # Act
    with pytest.raises(ValueError) as exc_info:
        RuleProcessor([rule], [])

    exception_raised = exc_info.value

    # Assert
    expected_message = "No datasets defined."
    assert exception_raised.args[0] == expected_message


def test_initialization_given_rule_dependencies():
    """Test if the processor can correctly initialize given
    the rule dependencies
    """

    # Arrange
    dataset = _xr.Dataset()
    dataset["test"] = _xr.DataArray([32, 94, 9])

    logger = Mock(ILogger)
    rules = _create_test_rules()
    processor = RuleProcessor(rules, [dataset])

    # Act & Assert
    assert processor.initialize(logger)


def test_process_rules_given_rule_dependencies():
    """Test if the processor can correctly process_rules given
    the rule dependencies
    """

    # Arrange
    input_dataset = _xr.Dataset()
    output_dataset = _xr.Dataset()

    input_dataset["test"] = _xr.DataArray([32, 94, 9])

    rule1 = Mock(IArrayBasedRule, id="rule1")
    rule2 = Mock(IArrayBasedRule, id="rule2")
    rule3 = Mock(IMultiArrayBasedRule, id="rule3")

    logger = Mock(ILogger)

    type(rule1).input_variable_names = ["test"]
    type(rule2).input_variable_names = ["test"]
    type(rule3).input_variable_names = ["out1", "out2"]

    type(rule1).output_variable_name = "out1"
    type(rule2).output_variable_name = "out2"
    type(rule3).output_variable_name = "out3"

    rule1.execute.return_value = _xr.DataArray([1, 2, 3])
    rule2.execute.return_value = _xr.DataArray([4, 5, 6])
    rule3.execute.return_value = _xr.DataArray([7, 8, 9])

    rules: List[IRule] = [rule1, rule2, rule3]
    processor = RuleProcessor(rules, [input_dataset])

    assert processor.initialize(logger)

    # Act
    processor.process_rules(output_dataset, logger)

    # Assert
    assert len(output_dataset) == 3
    for rule in rules:
        rule.execute.assert_called_once_with(ANY, logger)
        assert rule.output_variable_name in output_dataset.keys()


@pytest.mark.parametrize(
    "indices_to_remove, expected_result",
    [
        [[0], False],
        [[1], False],
        [[2], False],
        [[3], True],
        [[2, 3], True],
        [[1, 2, 3], True],
    ],
)
def test_initialization_for_different_rule_dependencies(
    indices_to_remove: List[int], expected_result: bool
):
    """Test if the processor can initialize given the rule dependencies"""

    # Arrange
    dataset = _xr.Dataset()
    dataset["test"] = _xr.DataArray([32, 94, 9])

    logger = Mock(ILogger)
    rules = _create_test_rules()
    processor = RuleProcessor(rules, [dataset])

    rules_to_remove = [rules[index] for index in indices_to_remove]

    # remove rules
    for rule in rules_to_remove:
        rules.remove(rule)

    # Act & Assert
    assert expected_result == processor.initialize(logger)


def test_process_rules_fails_for_uninitialized_processor():
    """Test if an error is thrown if process_rules is called on the processor
    when it is not properly initialized"""

    # Arrange
    input_dataset = _xr.Dataset()
    output_dataset = _xr.Dataset()
    input_dataset["test"] = _xr.DataArray([32, 94, 9])

    logger = Mock(ILogger)
    rule = Mock(IRule)

    processor = RuleProcessor([rule], [input_dataset])

    # Act
    with pytest.raises(RuntimeError) as exc_info:
        processor.process_rules(output_dataset, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "Processor is not properly initialized, please re-initialize"
    assert exception_raised.args[0] == expected_message


def test_process_rules_calls_multi_array_based_rule_execute_correctly():
    """Test if during processing the rule its execute method of
    an IMultiArrayBasedRule is called with the right parameter"""

    # Arrange
    input_dataset = _xr.Dataset()
    output_dataset = _xr.Dataset()
    array1 = _xr.DataArray([32, 94, 9])
    array2 = _xr.DataArray([7, 93, 6])

    input_dataset["test"] = array1
    input_dataset["test2"] = array2

    logger = Mock(ILogger)
    rule = Mock(IMultiArrayBasedRule)

    type(rule).input_variable_names = ["test", "test2"]
    type(rule).output_variable_name = "output"
    rule.execute.return_value = _xr.DataArray([4, 3, 2])

    processor = RuleProcessor([rule], [input_dataset])

    # Act
    assert processor.initialize(logger)
    processor.process_rules(output_dataset, logger)

    # Assert
    assert len(output_dataset) == 1
    assert rule.output_variable_name in output_dataset.keys()

    rule.execute.assert_called_once_with(ANY, logger)

    # get first call, first argument
    array_list: List[_xr.DataArray] = rule.execute.call_args[0][0]

    _xr.testing.assert_equal(array_list[0], array1)
    _xr.testing.assert_equal(array_list[1], array2)


def test_process_rules_calls_cell_based_rule_execute_correctly():
    """Test if during processing the rule its execute method of
    an ICellBasedRule is called with the right parameter"""

    # Arrange
    input_dataset = _xr.Dataset()
    output_dataset = _xr.Dataset()
    input_array = _xr.DataArray(_np.array([[1, 2, 3], [4, 5, 6]], _np.int32))

    input_dataset["test"] = input_array

    logger = Mock(ILogger)
    rule = Mock(ICellBasedRule)

    type(rule).input_variable_names = ["test"]
    type(rule).output_variable_name = "output"

    rule.execute.return_value = 1

    processor = RuleProcessor([rule], [input_dataset])

    # Act
    assert processor.initialize(logger)
    processor.process_rules(output_dataset, logger)

    # Assert
    assert len(output_dataset) == 1
    assert rule.output_variable_name in output_dataset.keys()

    assert rule.execute.call_count == 6


def test_process_rules_calls_array_based_rule_execute_correctly():
    """Test if during processing the rule its execute method of
    an IArrayBasedRule is called with the right parameter"""

    # Arrange
    input_dataset = _xr.Dataset()
    output_dataset = _xr.Dataset()
    input_array = _xr.DataArray([32, 94, 9])

    input_dataset["test"] = input_array

    logger = Mock(ILogger)
    rule = Mock(IArrayBasedRule)

    type(rule).input_variable_names = ["test"]
    type(rule).output_variable_name = "output"
    rule.execute.return_value = _xr.DataArray([4, 3, 2])

    processor = RuleProcessor([rule], [input_dataset])

    # Act
    assert processor.initialize(logger)
    processor.process_rules(output_dataset, logger)

    # Assert
    assert len(output_dataset) == 1
    assert rule.output_variable_name in output_dataset.keys()

    rule.execute.assert_called_once_with(ANY, logger)

    # get first call, first argument
    array: _xr.DataArray = rule.execute.call_args[0][0]

    _xr.testing.assert_equal(array, input_array)


def test_process_rules_throws_exception_for_array_based_rule_with_multiple_inputs():
    """Test if an error is thrown during processing of an IArrayBasedRule
    if two inputs were defined"""

    # Arrange
    input_dataset = _xr.Dataset()
    output_dataset = _xr.Dataset()

    input_dataset["test1"] = _xr.DataArray([32, 94, 9])
    input_dataset["test2"] = _xr.DataArray([32, 94, 9])

    logger = Mock(ILogger)
    rule = Mock(IArrayBasedRule)

    type(rule).input_variable_names = ["test1", "test2"]
    type(rule).output_variable_name = "output"

    processor = RuleProcessor([rule], [input_dataset])
    assert processor.initialize(logger)

    # Act
    with pytest.raises(NotImplementedError) as exc_info:
        processor.process_rules(output_dataset, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "Array based rule only supports one input"
    assert exception_raised.args[0] == expected_message


def test_process_rules_throws_exception_for_unsupported_rule():
    """Test if an error is thrown when trying to execute a rule that is
    not supported"""

    # Arrange
    input_dataset = _xr.Dataset()
    output_dataset = _xr.Dataset()
    input_array = _xr.DataArray([32, 94, 9])

    input_dataset["test"] = input_array

    logger = Mock(ILogger)
    rule = Mock(IRule)

    rule.name = "test"
    type(rule).input_variable_names = ["test"]
    type(rule).output_variable_name = "output"

    processor = RuleProcessor([rule], [input_dataset])
    assert processor.initialize(logger)

    # Act
    with pytest.raises(NotImplementedError) as exc_info:
        processor.process_rules(output_dataset, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "Can not execute rule test."
    assert exception_raised.args[0] == expected_message
