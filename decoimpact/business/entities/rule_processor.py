# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for RuleProcessor class

Classes:
    RuleProcessor

"""

from typing import Dict, Iterable, List, Tuple

import numpy as _np
import xarray as _xr

import decoimpact.business.utils.dataset_utils as _du
import decoimpact.business.utils.list_utils as _lu
from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.i_cell_based_rule import ICellBasedRule
from decoimpact.business.entities.rules.i_multi_array_based_rule import (
    IMultiArrayBasedRule,
)
from decoimpact.business.entities.rules.i_multi_cell_based_rule import (
    IMultiCellBasedRule,
)
from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.dictionary_utils import get_dict_element


class RuleProcessor:
    """Model class for processing models based on rules"""

    def __init__(self, rules: List[IRule], dataset: _xr.Dataset) -> None:
        """Creates instance of a rule processor using the provided
        rules and input datasets

        Args:
            rules (List[IRule]): rules to process
            input_dataset (_xr.Dataset): input dataset to use
        """
        if len(rules) < 1:
            raise ValueError("No rules defined.")

        if dataset is None:
            raise ValueError("No datasets defined.")

        self._rules = rules
        self._input_dataset = dataset
        self._processing_list: List[List[IRule]] = []

    def initialize(self, logger: ILogger) -> bool:
        """Creates an ordered list of rule arrays, where every rule array
        contains rules that can be processed simultaneously.

        Args:
            logger (ILogger): logger for reporting messages

        Returns:
            bool: A boolean to indicate if all the rules can be processed.
        """
        inputs: List[str] = []

        inputs = _lu.flatten_list(
            [_du.list_vars(self._input_dataset), _du.list_coords(self._input_dataset)]
        )

        tree, success = self._create_rule_sets(inputs, self._rules, [], logger)
        if success:
            self._processing_list = tree

        return success

    def process_rules(
        self, output_dataset: _xr.Dataset, logger: ILogger
    ) -> _xr.Dataset:
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
                    rule_result.coords,
                )
                for coord_key in rule_result.coords:
                    # the coord_key is overwritten in case we don't have the if
                    # statement below
                    if coord_key not in output_dataset.coords:
                        output_dataset = output_dataset.assign_coords(
                            {coord_key: rule_result[coord_key]}
                        )
        return output_dataset

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
            rules_list = [str(rule.name) for rule in unprocessed_rules]
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

        variable_lookup = dict(self._get_rule_input_variables(rule, output_dataset))
        variables = list(variable_lookup.values())

        if isinstance(rule, IMultiArrayBasedRule):
            result = rule.execute(variable_lookup, logger)

            # set output attributes, based on first array
            self._set_output_attributes(rule, result, variables[0])
            return result

        if isinstance(rule, IMultiCellBasedRule):
            result = self._process_by_multi_cell(rule, variable_lookup, logger)
            self._set_output_attributes(rule, result, variables[0])
            return result

        if len(variables) != 1:
            raise NotImplementedError("Array based rule only supports one input array.")

        input_variable = variables[0]
        if isinstance(rule, IArrayBasedRule):
            result = rule.execute(input_variable, logger)
            self._set_output_attributes(rule, result, input_variable)
            return result

        if isinstance(rule, ICellBasedRule):
            result = self._process_by_cell(rule, input_variable, logger)
            self._set_output_attributes(rule, result, input_variable)
            return result

        raise NotImplementedError(f"Can not execute rule {rule.name}.")

    def _set_output_attributes(
        self, rule: IRule, result: _xr.DataArray, input_variable: _xr.DataArray
    ):
        self._copy_definition_attributes(input_variable, result)

        result.attrs["long_name"] = rule.output_variable_name
        result.attrs["standard_name"] = rule.output_variable_name

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

        # define variables to count value exceedings (for some rules): min and max
        warning_counter_total = [0, 0]

        # execute rule and gather warnings for exceeded values (for some rules)
        for indices, value in _np.ndenumerate(np_array):
            result_variable[indices], warning_counter = rule.execute(value, logger)
            # update total counter for both min and max
            warning_counter_total[0] += warning_counter[0]
            warning_counter_total[1] += warning_counter[1]

        # show warnings values outside range (for some rules):
        if warning_counter_total[0] > 0:
            logger.log_warning(
                f"value less than min: {warning_counter_total[0]} occurence(s)"
            )
        if warning_counter_total[1] > 0:
            logger.log_warning(
                f"value greater than max: {warning_counter_total[1]} occurence(s)"
            )

        # use copy to get the same dimensions as the
        # original input variable
        return input_variable.copy(data=result_variable)

    def _process_by_multi_cell(
        self,
        rule: IMultiCellBasedRule,
        input_variables: Dict[str, _xr.DataArray],
        logger: ILogger,
    ) -> _xr.DataArray:
        """Processes every value of the input_variable and creates a
        new one from it

        Args:
            rule (IMultiCellBasedRule): rule to process
            input_variables (_xr.DataArray): input variables/data
            logger (ILogger): logger for log messages

        Returns:
            _xr.DataArray: _description_
        """
        if len(input_variables) < 1:
            raise NotImplementedError(
                f"Can not execute rule {rule.name} with no input variables."
            )

        value_arrays = list(input_variables.values())

        # Check the amount of dimensions of all variables
        len_dims = _np.array([len(vals.dims) for vals in value_arrays])

        # Use the variable with the most dimensions. Broadcast all other
        # variables to these dimensions
        most_dims_bool = len_dims == max(len_dims)

        ref_var = value_arrays[_np.argmax(len_dims)]
        for ind_vars, enough_dims in enumerate(most_dims_bool):
            if not enough_dims:
                var_orig = value_arrays[ind_vars]
                value_arrays[ind_vars] = self._expand_dimensions_of_variable(
                    var_orig, ref_var, logger
                )

        # Check if all variables now have the same dimensions
        self._check_variable_dimensions(value_arrays, rule)

        result_variable = _np.zeros_like(ref_var.to_numpy())
        cell_values = {}

        for indices, _ in _np.ndenumerate(ref_var.to_numpy()):
            for value in value_arrays:
                cell_values[value.name] = value.data[indices]

            result_variable[indices] = rule.execute(cell_values, logger)

        # use copy to get the same dimensions as the
        # original input variable
        return ref_var.copy(data=result_variable)

    def _get_rule_input_variables(
        self, rule: IRule, output_dataset: _xr.Dataset
    ) -> Iterable[Tuple[str, _xr.DataArray]]:
        input_variable_names = rule.input_variable_names

        for input_variable_name in input_variable_names:
            yield input_variable_name, self._get_variable_by_name(
                input_variable_name, output_dataset
            )

    def _get_variable_by_name(
        self, name: str, output_dataset: _xr.Dataset
    ) -> _xr.DataArray:
        # search output dataset (generated output)
        if name in output_dataset:
            return output_dataset[name]

        raise KeyError(
            f"Key {name} was not found in input datasets or "
            "in calculated output dataset.",
        )

    def _check_variable_dimensions(
        self, value_arrays: List[_xr.DataArray], rule: IMultiCellBasedRule
    ):
        for val_index in range(len(value_arrays) - 1):
            var1 = value_arrays[val_index]
            var2 = value_arrays[val_index + 1]
            diff = set(var1.dims) ^ set(var2.dims)

            # If the variables with the most dimensions have different dimensions,
            # stop the calculation
            if len(diff) != 0:
                raise NotImplementedError(
                    f"Can not execute rule {rule.name} with variables with different \
                    dimensions. Variable {var1.name} with dimensions:{var1.dims} is \
                    different than {var2.name} with dimensions:{var2.dims}"
                )

    def _expand_dimensions_of_variable(
        self, var_orig: _xr.DataArray, ref_var: _xr.DataArray, logger: ILogger
    ):
        """Creates a new data-array with the values of the var_org expanded to
        include all dimensions of the ref_var

        Args:
            var_orig (_xr.DataArray): variable to expand with extra dimensions
            ref_var (_xr.DataArray): reference variable to synchronize the
                                     dimensions with
            logger (ILogger): logger for logging messages
        """
        # Let the user know which variables will be broadcast to all dimensions
        dims_orig = var_orig.dims
        dims_result = ref_var.dims
        dims_diff = [str(x) for x in dims_result if x not in dims_orig]
        str_dims_broadcasted = ",".join(dims_diff)
        logger.log_info(
            f"""Variable {var_orig.name} will be expanded to the following \
            dimensions: {str_dims_broadcasted} """
        )

        # perform the broadcast
        var_broadcasted = _xr.broadcast(var_orig, ref_var)[0]

        # Make sure the dimensions are in the same order
        return var_broadcasted.transpose(*ref_var.dims)
