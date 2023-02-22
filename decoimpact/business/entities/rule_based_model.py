"""
Module for RuleBasedModel class

Classes:
    RuleBasedModel

"""

from typing import List

import xarray as _xr

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
        name: str = "Rule-Based model",
    ) -> None:

        self._name = name
        self._status = ModelStatus.CREATED
        self._rules = rules
        self._input_datasets: List[_xr.Dataset] = input_datasets
        self._output_dataset: _xr.Dataset = _xr.Dataset()
        self._rule_processor: RuleProcessor

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

        self._rule_processor = RuleProcessor(self._rules, self._input_datasets)
        success = self._rule_processor.initialize(logger)

        self._output_dataset = self.copy_dataset(self._input_datasets[0])
        # MDK 22-02-2023 NEEDS TO BE DONE AS PART OF DEI-32. Work in progess
        # Right now everything is copied to the output dataset, which is not ideal
        # self._output_dataset = self.remove_variable(
        #    self._output_dataset, list_variables
        # )

        if not success:
            logger.log_error("Initialization failed")

    def remove_variable(self, dataset: _xr.Dataset, variable: str) -> _xr.Dataset:
        """Remove variable from dataset

        Args:
            dataset (_xr.Dataset): Dataset to remove variable from
            variable (str/list): Variable(s) to remove

        Raises:
            ValueError: When variable can not be removed

        Returns:
            _xr.Dataset: Original dataset
        """
        try:
            dataset = dataset.drop_vars(variable)
        except ValueError as exc:
            raise ValueError("ERROR: Cannot remove variable from dataset") from exc
        return dataset

    def copy_dataset(self, dataset: _xr.Dataset) -> _xr.Dataset:
        """Copy dataset to new dataset

        Args:
            dataset (_xr.Dataset): Dataset to remove variable from
            variable (str): Variable to remove

        Raises:
            ValueError: When variable can not be removed

        Returns:
            _xr.Dataset: Original dataset
        """
        try:
            output_dataset = dataset.copy(deep=False)
        except ValueError as exc:
            raise ValueError("ERROR: Cannot copy dataset") from exc
        return output_dataset

    def execute(self, logger: ILogger) -> None:
        """Executes the model"""

        self._rule_processor.process_rules(self._output_dataset, logger)

    def finalize(self, logger: ILogger) -> None:
        """Finalizes the model"""

        logger.log_debug("Finalize the rule processor")
        self._rule_processor = None
