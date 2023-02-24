"""
Module for RuleBasedModel class

Classes:
    RuleBasedModel

"""

from typing import List

import xarray as _xr
from numpy import var

from decoimpact.business.entities.i_model import IModel, ModelStatus
from decoimpact.business.entities.rule_processor import RuleProcessor
from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.business.utils.dataset_utils import (
    list_vars,
    merge_list_of_datasets,
    remove_variables,
)
from decoimpact.business.utils.utils import flatten_list, remove_duplicates_from_list
from decoimpact.crosscutting.i_logger import ILogger


class RuleBasedModel(IModel):
    """Model class for models based on rules"""

    def __init__(
        self,
        input_datasets: List[_xr.Dataset],
        rules: List[IRule],
        mapping: dict[str, str] = {},
        name: str = "Rule-Based model",
    ) -> None:

        self._name = name
        self._status = ModelStatus.CREATED
        self._rules = rules
        self._input_datasets: List[_xr.Dataset] = input_datasets
        self._output_dataset: _xr.Dataset
        self._rule_processor: RuleProcessor
        self._mapping = mapping

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
            logger.log_error("Model does not contain any datasets")
            valid = False

        if len(self._rules) < 1:
            logger.log_error("Model does not contain any rules")
            valid = False

        for rule in self._rules:
            valid = valid and rule.validate(logger)

        return valid

    def initialize(self, logger: ILogger) -> None:
        """Initializes the model"""

        self._create_output_dataset()
        self._output_dataset = self._output_dataset.rename_vars(self._mapping)

        self._rule_processor = RuleProcessor(self._rules, self._input_datasets)
        success = self._rule_processor.initialize(logger)

        if not success:
            logger.log_error("Initialization failed")

    def _create_output_dataset(self):
        """Create the output dataset containing system variables"""
        self._output_dataset = merge_list_of_datasets(self._input_datasets)

        variables_in_output = self._make_output_variables_list()
        all_variables = list_vars(self._output_dataset)

        variables_to_remove = [x for x in all_variables if x not in variables_in_output]

        self._output_dataset = remove_variables(
            self._output_dataset, variables_to_remove
        )
        return self._output_dataset

    def _make_output_variables_list(self):
        """Make list of variables to be contained in the output dataset
        System variables have to be included in results to enable
        XUgrid support and prevent invalid topologies.
        This also allows QuickPlot to visualize the results.
        """
        system_vars = [
            "mesh2d",
            "mesh2d_face_nodes",
            "mesh2d_edge_nodes",
            "mesh2d_face_x_bnd",
            "mesh2d_face_y_bnd",
            "mesh2d_flowelem_bl",
        ]
        mapping_keys = list(self._mapping.keys())

        variables_in_output = []
        for rule in range(0, len(self._rules)):
            variables_in_output.append(self._rules[rule].input_variable_names)
            variables_in_output.append([self._rules[rule].output_variable_name])
        variables_in_output.append(system_vars)
        variables_in_output.append(mapping_keys)

        variables_in_output = flatten_list(
            remove_duplicates_from_list(variables_in_output)
        )
        return variables_in_output

    def execute(self, logger: ILogger) -> None:
        """Executes the model"""

        self._rule_processor.process_rules(self._output_dataset, logger)

    def finalize(self, logger: ILogger) -> None:
        """Finalizes the model"""

        logger.log_debug("Finalize the rule processor")
        self._rule_processor = None
