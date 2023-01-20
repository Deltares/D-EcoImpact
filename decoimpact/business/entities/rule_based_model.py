"""
Module for RuleBasedModel class

Classes:
    RuleBasedModel

"""
from typing import List

from decoimpact.business.entities.model_base import ModelBase
from decoimpact.business.entities.rules.rule_base import RuleBase


class RuleBasedModel(ModelBase):
    """Model class for models based on rules"""

    def __init__(self) -> None:

        super().__init__()

        self._rules = []
        self._name = "Rule-Based model"

    @property
    def rules(self) -> List[RuleBase]:
        """Rules to execute"""
        return self._rules

    @rules.setter
    def rules(self, rules: List[RuleBase]):
        """Rules to execute"""
        self._rules = rules

    def validate(self) -> bool:
        """Validates the model"""

    def initialize(self) -> None:
        """Initializes the model"""

    def execute(self) -> None:
        """Executes the model"""

    def finalize(self) -> None:
        """Finalizes the model"""
