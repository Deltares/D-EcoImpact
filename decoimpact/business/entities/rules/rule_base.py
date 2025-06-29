# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for RuleBase

Classes:
    RuleBase

"""

from abc import ABC
from typing import List

from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.crosscutting.i_logger import ILogger


class RuleBase(IRule, ABC):
    """Implementation of the rule base"""

    def __init__(self, name: str, input_variable_names: List[str]):
        self._name = name
        self._description = ""
        self._input_variable_names = input_variable_names
        self._output_variable_name = "output"

    @property
    def name(self) -> str:
        """Name of the rule"""
        return self._name

    @name.setter
    def name(self, name: str):
        """Name of the rule"""
        self._name = name

    @property
    def description(self) -> str:
        """Description of the rule"""
        return self._description

    @description.setter
    def description(self, description: str):
        """Description of the rule"""
        self._description = description

    @property
    def input_variable_names(self) -> List[str]:
        """Name of the input variable"""
        return self._input_variable_names

    @input_variable_names.setter
    def input_variable_names(self, input_variable_names: List[str]) -> List[str]:
        """Name of the input variables"""
        self._input_variable_names = input_variable_names

    @property
    def output_variable_name(self) -> str:
        """Name of the output variable"""
        return self._output_variable_name

    @output_variable_name.setter
    def output_variable_name(self, output_variable_name: str):
        """Name of the output variable"""
        self._output_variable_name = output_variable_name

    def validate(self, logger: ILogger) -> bool:
        """Validates if the rule is valid

        Returns:
            bool: wether the rule is valid
        """
        return True
