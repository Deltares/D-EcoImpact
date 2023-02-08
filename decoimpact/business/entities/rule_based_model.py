"""
Module for RuleBasedModel class

Classes:
    RuleBasedModel

"""
from typing import List

import xarray as _xr

from decoimpact.business.entities.i_model import IModel
from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.crosscutting.i_logger import ILogger


class RuleBasedModel(IModel):
    """Model class for models based on rules"""

    def __init__(self, logger: ILogger) -> None:

        super().__init__()

        self._rules = []
        self._name = "Rule-Based model"
        self._logger = logger

    @property
    def rules(self) -> List[IRule]:
        """Rules to execute"""
        return self._rules

    @rules.setter
    def rules(self, rules: List[IRule]):
        """Rules to execute"""
        self._rules = rules

    def validate(self) -> bool:
        """Validates the model"""
        return True

    def initialize(self) -> None:
        """Initializes the model"""

    def execute(self) -> None:
        """Executes the model"""
        for rule in self._rules:

            a = _xr.Array()

            if isinstance(rule, IArrayBasedRule):
                rule.execute(a, self._logger)

    def finalize(self) -> None:
        """Finalizes the model"""
