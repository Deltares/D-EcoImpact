"""
Module for RuleProcessor class

Classes:
    RuleProcessor

"""

from typing import Iterable, List, Tuple

import numpy as _np
import xarray as _xr

from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.i_cell_based_rule import ICellBasedRule
from decoimpact.business.entities.rules.i_multi_array_based_rule import (
    IMultiArrayBasedRule,
)
from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.dictionary_utils import get_dict_element


class RuleProcessor:
    """Model class for processing models based on rules"""

    def __init__(self, rules: List[IRule], input_dataset: _xr.Dataset) -> None:
        """Creates instance of a rule processor using the provided
        rules and input datasets

        Args:
            rules (List[IRule]): rules to process
            input_dataset (_xr.Dataset): input dataset to use
        """
        if len(rules) < 1:
            raise ValueError("No rules defined.")

        if input_dataset is None:
            raise ValueError("No datasets defined.")

        self._rules = rules
        self._input_dataset = input_dataset
        self._processing_list: List[List[IRule]] = []

    def initialize(self, logger: ILogger) -> bool:
        """Creates an ordered list of rule arrays, where every rule array contains
        rules that can be processed simultaneously.

        Args:
            logger (ILogger): logger for reporting messages

        Returns:
            bool: A boolean to indicate if all the rules can be processed.
        """
        inputs: List[str] = []

        for key in self._input_dataset:
            inputs.append(str(key))

        tree, success = self._create_rule_sets(inputs, list(self._rules), [], logger)
        if success:
            self._processing_list = tree

        return success

    def process_rules(self, output_dataset: _xr.Dataset, logger: ILogger) -> None:
        """Processes the rules defined in the initialize method
        and adds the results to the provided output_dataset.

        Args:
            output_dataset (_xr.Dataset): Dataset to place the rule
                                          results into
            logger (ILogger): logger for reporting messages

        Raises:
            RuntimeError: if initialization is not correctly done
        """
        if len(self._processing_list) < 1:
            message = "Processor is not properly initialized, please initialize."
            raise RuntimeError(message)

        for rule_set in self._processing_list:
            for rule in rule_set:
                logger.log_info(f"Starting rule {rule.name}")

                rule_result = self._execute_rule(rule, output_dataset, logger)
                output_name = rule.output_variable_name

                output_dataset[output_name] = (
                    rule_result.dims,
                    rule_result.values,
                    rule_result.attrs,
                )

    def _create_rule_sets(
        self,
        inputs: List[str],
        unprocessed_rules: List[IRule],
        current_tree: List[List[IRule]],
        logger: ILogger,
    ) -> Tuple[List[List[IRule]], bool]:
        """Creates an ordered list of rule-sets that can be processed in parallel.

        Args:
            inputs (List[str]): input names that are available to rules
            unprocessed_rules (List[IRule]): rules that still need to be handled
            current_tree (List[List[IRule]]): the current output list state
            logger (ILogger): logger for logging messages

        Returns:
            Tuple[List[List[IRule]], bool]: Ordered list of rule-sets
        """
        solvable_rules = self._get_solvable_rules(inputs, unprocessed_rules)

        if len(solvable_rules) == 0:
            rules_list = [rule.name for rule in unprocessed_rules]
            rules_text = ", ".join(rules_list)
            logger.log_warning(f"Some rules can not be resolved: {rules_text}")
            return [], False

        for rule in solvable_rules:
            unprocessed_rules.remove(rule)
            inputs.append(rule.output_variable_name)

        current_tree.append(solvable_rules)

        if len(unprocessed_rules) > 0:
            return self._create_rule_sets(
                inputs, unprocessed_rules, current_tree, logger
            )

        return current_tree, True

    def _get_solvable_rules(
        self, inputs: List[str], unprocessed_rules: List[IRule]
    ) -> List[IRule]:
        """Checks which rules can be resolved using the provided "inputs" list.

        Args:
            inputs (List[str]): available inputs to resolve rules with
            unprocessed_rules (List[IRule]): rules that need need to be checked

        Returns:
            List[IRule]: list of rules that can be resolved with the provided inputs
        """
        solvable_rules: List[IRule] = []

        for rule in unprocessed_rules:
            names = rule.input_variable_names

            if all(name in inputs for name in names):
                solvable_rules.append(rule)

        return solvable_rules

    def _execute_rule(
        self, rule: IRule, output_dataset: _xr.Dataset, logger: ILogger
    ) -> _xr.DataArray:
        """Processes the rule with the provided dataset.

        Returns:
            _xr.DataArray: result data set
        """

        variables = list(self._get_rule_input_variables(rule, output_dataset))

        if isinstance(rule, IMultiArrayBasedRule):
            return rule.execute(variables, logger)

        if len(variables) != 1:
            raise NotImplementedError("Array based rule only supports one input array.")

        input_variable = variables[0]

        if isinstance(rule, IArrayBasedRule):
            result = rule.execute(input_variable, logger)
            self._copy_definition_attributes(input_variable, result)
            return result

        if isinstance(rule, ICellBasedRule):
            result = self._process_by_cell(rule, input_variable, logger)
            self._copy_definition_attributes(input_variable, result)
            return result

        raise NotImplementedError(f"Can not execute rule {rule.name}.")

    def _copy_definition_attributes(
        self, source_array: _xr.DataArray, target_array: _xr.DataArray
    ) -> None:
        attributes_to_copy = ["location", "mesh"]

        for attribute_name in attributes_to_copy:
            target_array.attrs[attribute_name] = get_dict_element(
                attribute_name, source_array.attrs, False
            )

    def _process_by_cell(
        self, rule: ICellBasedRule, input_variable: _xr.DataArray, logger: ILogger
    ) -> _xr.DataArray:
        """Processes every value of the input_variable and creates a
        new one from it

        Args:
            rule (ICellBasedRule): rule to process
            input_variable (_xr.DataArray): input variable/data
            logger (ILogger): logger for log messages

        Returns:
            _xr.DataArray: _description_
        """
        np_array = input_variable.to_numpy()
        result_variable = _np.zeros_like(np_array)

        for indices, value in _np.ndenumerate(np_array):
            result_variable[indices] = rule.execute(value, logger)

        # use copy to get the same dimensions as the
        # original input variable
        return input_variable.copy(data=result_variable)

    def _get_rule_input_variables(
        self, rule: IRule, output_dataset: _xr.Dataset
    ) -> Iterable[_xr.DataArray]:
        input_variable_names = rule.input_variable_names

        for input_variable_name in input_variable_names:
            yield self._get_variable_by_name(input_variable_name, output_dataset)

    def _get_variable_by_name(
        self, name: str, output_dataset: _xr.Dataset
    ) -> _xr.DataArray:
        # search output dataset (generated output)
        if name in output_dataset:
            return output_dataset[name]

        raise KeyError(
            f"Key {name} was not found in input datasets or ",
            "in calculated output dataset.",
        )
