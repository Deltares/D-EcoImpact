# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for RuleBasedModel class

Classes:
    RuleBasedModel

"""

from typing import List, Optional

import xarray as _xr

import decoimpact.business.utils.dataset_utils as _du
import decoimpact.business.utils.list_utils as _lu
from decoimpact.business.entities.i_model import IModel, ModelStatus
from decoimpact.business.entities.rule_processor import RuleProcessor
from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.crosscutting.i_logger import ILogger


class RuleBasedModel(IModel):
    """Model class for models based on rules"""

    def __init__(
        self,
        input_datasets: List[_xr.Dataset],
        rules: List[IRule],
        mapping: Optional[dict[str, str]] = None,
        name: str = "Rule-Based model",
    ) -> None:

        self._name = name
        self._status = ModelStatus.CREATED
        self._rules = rules
        self._input_datasets: List[_xr.Dataset] = input_datasets
        self._output_dataset: _xr.Dataset
        self._rule_processor: Optional[RuleProcessor]
        self._mappings = mapping

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
        """Input datasets for the model"""
        return self._input_datasets

    @property
    def output_dataset(self) -> _xr.Dataset:
        """Output dataset produced by this model"""
        return self._output_dataset

    def validate(self, logger: ILogger) -> bool:
        """Validates the model"""

        valid = True

        if len(self._input_datasets) < 1:
            logger.log_error("Model does not contain any datasets.")
            valid = False

        if len(self._rules) < 1:
            logger.log_error("Model does not contain any rules.")
            valid = False

        for rule in self._rules:
            valid = rule.validate(logger) and valid

        if self._mappings is not None:
            valid = self._validate_mappings(self._mappings, logger) and valid

        return valid

    def initialize(self, logger: ILogger) -> None:
        """Initializes the model.
        Creates an output dataset which contains the necessary variables obtained
        from the input dataset.
        """

        self._output_dataset = _du.create_composed_dataset(
            self._input_datasets, self._make_output_variables_list(), self._mappings
        )
        self._rule_processor = RuleProcessor(self._rules, self._output_dataset)
        success = self._rule_processor.initialize(logger)

        if not success:
            logger.log_error("Initialization failed.")

    def execute(self, logger: ILogger) -> None:
        """Executes the model"""
        if self._rule_processor is None:
            raise RuntimeError("Processor is not set, please initialize model.")

        self._output_dataset = self._rule_processor.process_rules(
            self._output_dataset, logger
        )

    def finalize(self, logger: ILogger) -> None:
        """Finalizes the model"""

        logger.log_debug("Finalize the rule processor.")
        self._rule_processor = None

    def _make_output_variables_list(self):
        """Make the list of variables to be contained in the output dataset.
        A list of variables needed is obtained from the dummy variable and
        the dependent variables are recursively looked up. This is done to
        support XUgrid and to prevent invalid topologies.
        This also allows QuickPlot to visualize the results.
        """

        var_list = []
        dummy_vars = []

        for dataset in self._input_datasets:
            dummy_vars = _du.get_dummy_variable_in_ugrid(dataset)
            var_list = _du.rec_search_dep_vars(dataset, dummy_vars, [], [])

        mapping_keys = list((self._mappings or {}).keys())
        all_vars = dummy_vars + var_list + mapping_keys + self._get_direct_rule_inputs()
        return _lu.remove_duplicates_from_list(all_vars)

    def _validate_mappings(self, mappings: dict[str, str], logger: ILogger) -> bool:
        """Checks if the provided mappings are valid.

        Args:
            mappings (dict[str, str]): mappings to check
            logger (ILogger): logger for logging messages

        Returns:
            bool: if mappings are valid
        """
        input_vars = _lu.flatten_list(
            [_du.list_vars(ds) for ds in self._input_datasets]
        )

        valid = True

        # check if mapping keys are available in the input datasets
        mapping_vars_expected = list(mappings.keys())
        missing_vars = _lu.items_not_in(mapping_vars_expected, input_vars)

        if len(missing_vars) > 0:
            logger.log_error(
                "Could not find mapping variables "
                f"'{', '.join(missing_vars)}' in any input dataset."
            )
            valid = False

        # check for duplicates that will be created because of mapping
        mapping_vars_created = list(mappings.values())
        duplicates_created = _lu.items_in(mapping_vars_created, input_vars)

        if len(duplicates_created) > 0:
            logger.log_error(
                "Mapping towards the following variables "
                f"'{', '.join(duplicates_created)}', will create duplicates with"
                " variables in the input datasets."
            )
            valid = False

        # check for missing rule inputs
        needed_rule_inputs = _lu.remove_duplicates_from_list(
            self._get_direct_rule_inputs()
        )
        rule_input_vars = input_vars + mapping_vars_created
        missing_rule_inputs = _lu.items_not_in(needed_rule_inputs, rule_input_vars)
        if len(missing_rule_inputs) > 0:
            logger.log_error(
                f"Missing the variables '{', '.join(missing_rule_inputs)}' that "
                "are required by some rules."
            )
            valid = False

        return valid

    def _get_direct_rule_inputs(self) -> List[str]:
        """Gets the input variables directly needed by rules from
        input datasets.

        Returns:
            List[str]:
        """
        rule_input_vars = _lu.flatten_list(
            [rule.input_variable_names for rule in self._rules]
        )
        rule_output_vars = [rule.output_variable_name for rule in self._rules]

        return _lu.items_not_in(rule_input_vars, rule_output_vars)
