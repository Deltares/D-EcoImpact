# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for RuleBasedModel class
"""


from typing import Dict, List
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
from decoimpact.business.entities.rules.i_multi_cell_based_rule import (
    IMultiCellBasedRule,
)
from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.business.entities.rules.time_aggregation_rule import TimeAggregationRule
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_time_aggregation_rule_data import ITimeAggregationRuleData


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

    rule1.input_variable_names = ["test"]
    rule2.input_variable_names = ["test"]
    rule3.input_variable_names = ["out1", "out2"]
    rule4.input_variable_names = ["out3", "test"]

    rule1.output_variable_name = "out1"
    rule2.output_variable_name = "out2"
    rule3.output_variable_name = "out3"
    rule4.output_variable_name = "out4"

    rule1.name = "rule1"
    rule2.name = "rule2"
    rule3.name = "rule3"
    rule4.name = "rule4"

    return [rule1, rule2, rule3, rule4]


def test_creating_rule_processor_without_rules_should_throw_exception():
    """
    Tests if absence of rules is correctly checked during creation of the processor.
    """

    # Arrange
    dataset = _xr.Dataset()
    dataset["test"] = _xr.DataArray([32, 94, 9])

    rules = []

    # Act
    with pytest.raises(ValueError) as exc_info:
        RuleProcessor(rules, dataset)

    exception_raised = exc_info.value

    # Assert
    expected_message = "No rules defined."
    assert exception_raised.args[0] == expected_message


def test_creating_rule_processor_without_input_datasets_should_throw_exception():
    """
    Tests if input datasets are correctly checked during creation of the processor.
    """

    # Arrange
    rule = Mock(IRule)

    # Act
    with pytest.raises(ValueError) as exc_info:
        RuleProcessor([rule], None)

    exception_raised = exc_info.value

    # Assert
    expected_message = "No datasets defined."
    assert exception_raised.args[0] == expected_message


def test_initialization_given_rule_dependencies():
    """Tests if the processor can correctly initialize given
    the rule dependencies.
    """

    # Arrange
    dataset = _xr.Dataset()
    dataset["test"] = _xr.DataArray([32, 94, 9])

    logger = Mock(ILogger)
    rules = _create_test_rules()
    processor = RuleProcessor(rules, dataset)

    # Act & Assert
    assert processor.initialize(logger)


def test_process_rules_given_rule_dependencies():
    """Tests if the processor can correctly process_rules given
    the rule dependencies.
    """

    # Arrange
    dataset = _xr.Dataset()
    dataset["test"] = _xr.DataArray([32, 94, 9])

    rule1 = Mock(IArrayBasedRule, id="rule1")
    rule2 = Mock(IArrayBasedRule, id="rule2")
    rule3 = Mock(IMultiArrayBasedRule, id="rule3")

    logger = Mock(ILogger)

    rule1.input_variable_names = ["test"]
    rule2.input_variable_names = ["test"]
    rule3.input_variable_names = ["out1", "out2"]

    rule1.output_variable_name = "out1"
    rule2.output_variable_name = "out2"
    rule3.output_variable_name = "out3"

    rule1.execute.return_value = _xr.DataArray([1, 2, 3])
    rule2.execute.return_value = _xr.DataArray([4, 5, 6])
    rule3.execute.return_value = _xr.DataArray([7, 8, 9])

    rules: List[IRule] = [rule1, rule2, rule3]
    processor = RuleProcessor(rules, dataset)

    assert processor.initialize(logger)

    # Act
    processor.process_rules(dataset, logger)

    # Assert
    assert len(dataset) == 4
    for rule in [rule1, rule2, rule3]:
        rule.execute.assert_called_once_with(ANY, logger)
        assert rule.output_variable_name in dataset.keys()


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
    """Tests if the processor can initialize given the rule dependencies."""

    # Arrange
    dataset = _xr.Dataset()
    dataset["test"] = _xr.DataArray([32, 94, 9])

    logger = Mock(ILogger)
    rules = _create_test_rules()
    processor = RuleProcessor(rules, dataset)

    rules_to_remove = [rules[index] for index in indices_to_remove]

    # remove rules
    for rule in rules_to_remove:
        rules.remove(rule)

    # Act & Assert
    assert expected_result == processor.initialize(logger)


def test_process_rules_fails_for_uninitialized_processor():
    """Tests if an error is thrown if process_rules is called on the processor
    when it is not properly initialized."""

    # Arrange
    input_dataset = _xr.Dataset()
    output_dataset = _xr.Dataset()
    input_dataset["test"] = _xr.DataArray([32, 94, 9])

    logger = Mock(ILogger)
    rule = Mock(IRule)

    processor = RuleProcessor([rule], input_dataset)

    # Act
    with pytest.raises(RuntimeError) as exc_info:
        processor.process_rules(output_dataset, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "Processor is not properly initialized, please initialize."
    assert exception_raised.args[0] == expected_message


def test_process_rules_calls_multi_array_based_rule_execute_correctly():
    """Tests if during processing the rule its execute method of
    an IMultiArrayBasedRule is called with the right parameters."""

    # Arrange
    dataset = _xr.Dataset()
    array1 = _xr.DataArray([32, 94, 9])
    array2 = _xr.DataArray([7, 93, 6])

    dataset["test1"] = array1
    dataset["test2"] = array2

    logger = Mock(ILogger)
    rule = Mock(IMultiArrayBasedRule)

    rule.input_variable_names = ["test1", "test2"]
    rule.output_variable_name = "output"
    rule.execute.return_value = _xr.DataArray([4, 3, 2])

    processor = RuleProcessor([rule], dataset)

    # Act
    assert processor.initialize(logger)
    processor.process_rules(dataset, logger)

    # Assert
    assert len(dataset) == 3
    assert rule.output_variable_name in dataset.keys()

    rule.execute.assert_called_once_with(ANY, logger)

    # get first call, first argument
    array_lookup: Dict[str, _xr.DataArray] = rule.execute.call_args[0][0]

    _xr.testing.assert_equal(array_lookup["test1"], array1)
    _xr.testing.assert_equal(array_lookup["test2"], array2)


def test_process_rules_calls_cell_based_rule_execute_correctly():
    """Tests if during processing the rule its execute method of
    an ICellBasedRule is called with the right parameter."""

    # Arrange
    dataset = _xr.Dataset()
    input_array = _xr.DataArray(_np.array([[1, 2, 3], [4, 5, 6]], _np.int32))

    dataset["test"] = input_array

    logger = Mock(ILogger)
    rule = Mock(ICellBasedRule)

    rule.input_variable_names = ["test"]
    rule.output_variable_name = "output"

    rule.execute.return_value = [1, 0, 0]

    processor = RuleProcessor([rule], dataset)

    # Act
    assert processor.initialize(logger)
    processor.process_rules(dataset, logger)

    # Assert
    assert len(dataset) == 2
    assert rule.output_variable_name in dataset.keys()

    assert rule.execute.call_count == 6


def test_process_rules_calls_multi_cell_based_rule_execute_correctly():
    """Tests if during processing the rule its execute method of
    an IMultiCellBasedRule is called with the right parameter."""

    # Arrange
    dataset = _xr.Dataset()
    input_array1 = _xr.DataArray(_np.array([[1, 2, 3], [4, 5, 6]], _np.int32))
    input_array2 = _xr.DataArray(_np.array([[1, 2, 3], [4, 5, 6]], _np.int32))

    dataset["test1"] = input_array1
    dataset["test2"] = input_array2

    logger = Mock(ILogger)
    rule = Mock(IMultiCellBasedRule)

    rule.input_variable_names = ["test1", "test2"]
    rule.output_variable_name = "output"

    rule.execute.return_value = 1

    processor = RuleProcessor([rule], dataset)

    # Act
    assert processor.initialize(logger)
    processor.process_rules(dataset, logger)

    # Assert
    assert len(dataset) == 3
    assert rule.output_variable_name in dataset.keys()

    assert rule.execute.call_count == 6


def test_process_rules_calls_array_based_rule_execute_correctly():
    """Tests if during processing the rule its execute method of
    an IArrayBasedRule is called with the right parameter."""

    # Arrange
    output_dataset = _xr.Dataset()
    input_array = _xr.DataArray([32, 94, 9])

    output_dataset["test"] = input_array

    logger = Mock(ILogger)
    rule = Mock(IArrayBasedRule)

    rule.input_variable_names = ["test"]
    rule.output_variable_name = "output"
    rule.execute.return_value = _xr.DataArray([4, 3, 2])

    processor = RuleProcessor([rule], output_dataset)

    # Act
    assert processor.initialize(logger)
    processor.process_rules(output_dataset, logger)

    # Assert
    assert len(output_dataset) == 2
    assert rule.output_variable_name in output_dataset.keys()

    rule.execute.assert_called_once_with(ANY, logger)

    # get first call, first argument
    array: _xr.DataArray = rule.execute.call_args[0][0]

    _xr.testing.assert_equal(array, input_array)


def test_process_rules_throws_exception_for_array_based_rule_with_multiple_inputs():
    """Tests if an error is thrown during processing of an IArrayBasedRule
    if two inputs were defined."""

    # Arrange
    output_dataset = _xr.Dataset()

    output_dataset["test1"] = _xr.DataArray([32, 94, 9])
    output_dataset["test2"] = _xr.DataArray([32, 94, 9])

    logger = Mock(ILogger)
    rule = Mock(IArrayBasedRule)

    rule.input_variable_names = ["test1", "test2"]
    rule.output_variable_name = "output"

    processor = RuleProcessor([rule], output_dataset)
    assert processor.initialize(logger)

    # Act
    with pytest.raises(NotImplementedError) as exc_info:
        processor.process_rules(output_dataset, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = "Array based rule only supports one input array."
    assert exception_raised.args[0] == expected_message


def test_process_rules_throws_exception_for_unsupported_rule():
    """Tests if an error is thrown when trying to execute a rule that is
    not supported."""

    # Arrange
    output_dataset = _xr.Dataset()
    input_array = _xr.DataArray([32, 94, 9])

    output_dataset["test"] = input_array

    logger = Mock(ILogger)
    rule = Mock(IRule)

    rule.name = "test"
    rule.input_variable_names = ["test"]
    rule.output_variable_name = "output"

    processor = RuleProcessor([rule], output_dataset)
    assert processor.initialize(logger)

    # Act
    with pytest.raises(NotImplementedError) as exc_info:
        processor.process_rules(output_dataset, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = f"Can not execute rule {rule.name}."
    assert exception_raised.args[0] == expected_message


def test_process_rules_copies_multi_coords_correctly():
    """Tests if during processing the coords are copied to the output array
    and there are no duplicates."""

    # Arrange
    output_dataset = _xr.Dataset()
    output_dataset["test"] = _xr.DataArray([32, 94, 9])

    logger = Mock(ILogger)
    rule = Mock(IArrayBasedRule)
    rule_2 = Mock(IArrayBasedRule)

    result_array = _xr.DataArray([27, 45, 93])
    result_array = result_array.assign_coords({"test": _xr.DataArray([2, 4, 5])})

    result_array_2 = _xr.DataArray([1, 2, 93])
    result_array_2 = result_array.assign_coords({"test": _xr.DataArray([2, 4, 5])})

    rule.input_variable_names = ["test"]
    rule.output_variable_name = "output"
    rule.execute.return_value = result_array

    rule_2.input_variable_names = ["test"]
    rule_2.output_variable_name = "output_2"
    rule_2.execute.return_value = result_array_2

    processor = RuleProcessor([rule, rule_2], output_dataset)

    # Act
    assert processor.initialize(logger)
    result_dataset = processor.process_rules(output_dataset, logger)

    # Assert
    assert "test" in result_dataset.coords
    # compare coords at the level of variable
    result_array_coords = result_array.coords["test"]
    result_output_var_coords = result_dataset.output.coords["test"]  # output variable
    assert (result_output_var_coords == result_array_coords).all()

    # compare coords at the level of dataset /
    # check if the coordinates are correctly copied to the dataset
    result_dataset_coords = result_dataset.coords["test"]
    assert (result_output_var_coords == result_dataset_coords).all()

    # check if havnig an extra rule with coordinates then they are not copy pasted too
    assert len(result_dataset.output.coords) == 1


def test_execute_rule_throws_error_for_unknown_input_variable():
    """Tests that trying to execute a rule with an unknown input variable
    throws an error, and the error message."""

    # Arrange
    output_dataset = _xr.Dataset()
    input_array = _xr.DataArray([32, 94, 9])

    output_dataset["test"] = input_array

    logger = Mock(ILogger)
    rule = Mock(IRule)

    rule.name = "test"
    rule.input_variable_names = ["unexisting"]
    rule.output_variable_name = "output"

    processor = RuleProcessor([rule], output_dataset)

    # Act
    with pytest.raises(KeyError) as exc_info:
        processor._execute_rule(rule, output_dataset, logger)

    exception_raised = exc_info.value

    # Assert
    expected_message = (
        f"Key {rule.input_variable_names[0]} was not found "
        + "in input datasets or in calculated output dataset."
    )
    assert exception_raised.args[0] == expected_message
