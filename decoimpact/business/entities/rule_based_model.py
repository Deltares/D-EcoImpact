"""
Module for RuleBasedModel class

Classes:
    RuleBasedModel

"""

from typing import Iterable, List, Tuple

import xarray as _xr

from decoimpact.business.entities.i_model import IModel, ModelStatus
from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.i_multi_array_based_rule import (
    IMultiArrayBasedRule,
)
from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.crosscutting.i_logger import ILogger


class RuleBasedModel(IModel):
    """Model class for models based on rules"""

    def __init__(
        self,
        input_datasets: List[_xr.Dataset],
        rules: List[IRule],
        name: str = "Rule-Based model",
    ) -> None:

        self._name = name
        self._status = ModelStatus.CREATED
        self._rules = rules
        self._input_datasets: List[_xr.Dataset] = input_datasets
        self._output_dataset = _xr.Dataset()
        self._processing_list: List[List[IRule]] = []

    @property
    def name(self) -> str:
        """Name of the model"""
        return self._name

    @property
    def status(self) -> ModelStatus:
        """Status of the model"""
        return self._status

    @status.setter
    def status(self, status: ModelStatus):
        """Status of the model"""
        self._status = status

    @property
    def rules(self) -> List[IRule]:
        """Rules to execute"""
        return self._rules

    @property
    def input_datasets(self) -> List[_xr.Dataset]:
        """Status of the model"""
        return self._input_datasets

    def validate(self, logger: ILogger) -> bool:
        """Validates the model"""

        success = len(self._input_datasets) >= 1
        success = success and len(self._rules) >= 1

        for rule in self._rules:
            success = success and rule.validate()

        # check if rules can be resolved
        if success:
            tree, result = self._get_processing_list(logger)
            self._processing_list = tree
            success = success and result

        return success

    def initialize(self, logger: ILogger) -> None:
        """Initializes the model"""

        if len(self._processing_list) != 0:
            return

        self._processing_list, success = self._get_processing_list(logger)

        if not success:
            logger.log_error("Initialization failed")

    def execute(self, logger: ILogger) -> None:
        """Executes the model"""

        for rule_set in self._processing_list:
            for rule in rule_set:
                logger.log_info(f"Starting rule {rule.name}")

                rule_result = self._execute_rule(rule, logger)
                output_name = rule.output_variable_name

                self._output_dataset[output_name] = (
                    rule_result.dims,
                    rule_result.values,
                )

    def finalize(self, logger: ILogger) -> None:
        """Finalizes the model"""
        # write output to file


class RuleBuilder:

    def _get_processing_list(self, logger: ILogger) -> Tuple[List[List[IRule]], bool]:
        """Creates an ordered list of rules arrays, where every rule array contains rules
        that can be processed simultaneously.

        Args:
            logger (ILogger): logger for reporting messages

        Returns:
            Tuple[List[List[IRule]], bool]: List of rule arrays ordered by
            processing order. Also returns a boolean to indicate if all the
            rules can be processed.
        """
        inputs: List[str] = []
        for dataset in self._input_datasets:
            for key in dataset:
                inputs.append(str(key))

        return self._process_rules(inputs, list(self._rules), [], logger)

    def _process_rules(
        self,
        inputs: List[str],
        unprocessed_rules: List[IRule],
        current_tree: List[List[IRule]],
        logger: ILogger,
    ) -> Tuple[List[List[IRule]], bool]:

        solvable_rules = self._get_solvable_rules(inputs, unprocessed_rules)

        if len(solvable_rules) == 0:
            logger.log_warning("Can not resolve all rules")
            return [], False

        for rule in solvable_rules:
            unprocessed_rules.remove(rule)
            inputs.append(rule.output_variable_name)

        current_tree.append(solvable_rules)

        if len(unprocessed_rules) > 0:
            return self._process_rules(inputs, unprocessed_rules, current_tree, logger)

        return current_tree, True

    def _get_solvable_rules(
        self, inputs: List[str], unprocessed_rules: List[IRule]
    ) -> List[IRule]:

        solvable_rules: List[IRule] = []

        for rule in unprocessed_rules:
            names = rule.input_variable_names

            if all(name in inputs for name in names):
                solvable_rules.append(rule)

        return solvable_rules

    def _execute_rule(self, rule: IRule, logger: ILogger) -> _xr.DataArray:
        """Processes the rule with the provided dataset

        Returns:
            _xr.DataArray: result data set
        """

        variables = list(self._get_rule_input_variables(rule))

        if isinstance(rule, IMultiArrayBasedRule):
            return rule.execute(variables, logger)

        if len(variables) != 1:
            raise NotImplementedError("Array based rule only supports one input")

        if isinstance(rule, IArrayBasedRule):
            return rule.execute(variables[0], logger)

        # todo: add cellbase rule running logic
        # if isinstance(rule, ICellBasedRule):
        #     return self._process_by_cell(rule, input_variable, self._dataset)

        raise NotImplementedError(f"Can not execute rule {rule.name}.")

    def _get_rule_input_variables(self, rule: IRule) -> Iterable[_xr.DataArray]:
        input_variable_names = rule.input_variable_names

        for input_variable_name in input_variable_names:
            yield self._get_variable_by_name(input_variable_name)

    def _get_variable_by_name(self, name: str) -> _xr.DataArray:
        # search input datasets
        for dataset in self._input_datasets:
            if name in dataset.keys():
                return dataset[name]

        # search output dataset (generated output)
        if name in self._output_dataset:
            return self._output_dataset[name]

        raise KeyError(f"Key {name} was not found in ")
