"""
Module for RuleBasedModel class

Classes:
    RuleBasedModel

"""
from typing import List

import xarray as _xr

from decoimpact.business.entities.i_model import IModel, ModelStatus
from decoimpact.business.entities.rules.i_rule import IRule


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
        print(rules)
        self._rules = rules
        self._input_datasets: List[_xr.Dataset] = input_datasets

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

    def validate(self) -> bool:
        """Validates the model"""

        success = len(self._input_datasets) >= 1
        success &= len(self._rules) >= 1

        return success

    def initialize(self) -> None:
        """Initializes the model"""

    def execute(self) -> None:
        """Executes the model"""

    def finalize(self) -> None:
        """Finalizes the model"""
