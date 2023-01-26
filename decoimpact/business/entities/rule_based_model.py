"""
Module for RuleBasedModel class

Classes:
    RuleBasedModel

"""
from typing import List

from decoimpact.business.entities.i_model import IModel
from decoimpact.business.entities.rules.i_rule import IRule


class RuleBasedModel(IModel):
    """Model class for models based on rules"""

    def __init__(self) -> None:

        super().__init__()

        self._rules = []
        self._name = "Rule-Based model"

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

    def finalize(self) -> None:
        """Finalizes the model"""
