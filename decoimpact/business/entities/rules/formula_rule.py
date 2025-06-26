# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for Formula Rule class

Classes:
    Formula Rule
"""

# Import safe modules
import math
from argparse import ArgumentError as _ArgumentError
from typing import Dict, List

import numpy
from RestrictedPython import compile_restricted as _compile_restricted
from RestrictedPython import safe_builtins as _safe_builtins

from decoimpact.business.entities.rules.i_multi_cell_based_rule import (
    IMultiCellBasedRule,
)
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.crosscutting.i_logger import ILogger

# disabled pylint warning about use of exec.
# pylint: disable=W0122


class FormulaRule(RuleBase, IMultiCellBasedRule):
    """Implementation for the Formula rule"""

    formula_output_name: str = "formula_result"

    def __init__(self, name: str, input_variable_names: List[str], formula: str):
        super().__init__(name, input_variable_names)
        self._formula = formula
        self._byte_code = None
        self._setup_environment()

    def validate(self, logger: ILogger) -> bool:
        try:
            byte_code = _compile_restricted(
                f"{self.formula_output_name} = {self._formula}",
                filename="<inline code>",
                mode="exec",
            )
            local_variables = dict.fromkeys(self.input_variable_names, 1.0)
            exec(byte_code, self._global_variables, local_variables)

        except (SyntaxError, NameError) as exception:
            logger.log_error(f"Could not create formula function: {exception}")
            return False

        return True

    @property
    def formula(self) -> str:
        """Multiplier property"""
        return self._formula

    def execute(self, values: Dict[str, float], logger: ILogger) -> float:
        """Calculates the formula based on the
        Args:
            values (DataArray): values to Formula
        Returns:
            float: Calculated float
        """

        if not self._byte_code:
            self._byte_code = _compile_restricted(
                f"{self.formula_output_name} = {self._formula}",
                filename="<inline code>",
                mode="exec",
            )

        local_variables = values.copy()

        try:
            exec(self._byte_code, self._global_variables, local_variables)

        except SyntaxError as exception:
            logger.log_error(f"The formula can not be executed. {exception}")

        return float(local_variables[self.formula_output_name])

    def _setup_environment(self):
        # use standard libraries that are considered safe
        self._safe_modules_dict = {
            "math": math,
            "numpy": numpy,
        }

        # Global data available in restricted code
        self._global_variables = {
            "__builtins__": {**_safe_builtins, "__import__": self._safe_import},
            **self._safe_modules_dict,
        }

        self._byte_code = None

    def _safe_import(self, name, *args, **kwargs):
        # Redefine import, to only import from safe modules
        if name not in self._safe_modules_dict:
            raise _ArgumentError(None, f"Importing {name!r} is not allowed!")
        return __import__(name, *args, **kwargs)
