"""
Module for Formula Rule class

Classes:
    Formula Rule
"""

from typing import List, Dict

import xarray as _xr

from decoimpact.business.entities.rules.i_array_based_rule import IArrayBasedRule
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.crosscutting.i_logger import ILogger
from argparse import ArgumentError as _ArgumentError

from RestrictedPython import compile_restricted as _compile_restricted
from RestrictedPython import safe_builtins as _safe_builtins


class FormulaRule(RuleBase, IArrayBasedRule):
    """Implementation for the Formula rule"""

    def __init__(
        self,
        name: str,
        input_variable_names: List[str],
        formula: str,
        output_variable_name: str = "output",
        description: str = "",
    ):
        super().__init__(name, input_variable_names, output_variable_name, description)
        self._formula = formula
        self._SAFE_MODULES = frozenset(
            (
                "math",
                "numpy",
            )
        )

    @property
    def formula(self) -> str:
        """Multiplier property"""
        return self._formula

    def execute_single_input(
        self, value: _xr.DataArray, logger: ILogger
    ) -> _xr.DataArray:
        value_arrays = {self.input_variable_names[0]: value}
        return self.execute_multiple_input(value_arrays, logger)

    def execute_multiple_input(
        self, value_arrays: Dict[str, _xr.DataArray], logger: ILogger
    ) -> _xr.DataArray:

        """Calculates the formula based on the
        Args:
            value_arrays (DataArray): values to Formula
        Returns:
            DataArray: Calculated array
        """
        # Global data available in restricted code
        my_globals = {  # MDK: THIS NEEDS TO CHANGE TO A MORE GENERAL APPROACH
            "__builtins__": {
                **_safe_builtins,
                "__import__": self._safe_import,
                **value_arrays,
            },
        }

        ldict = {}

        try:
            byte_code = _compile_restricted(f"output = {self._formula}", mode="exec")
            exec(byte_code, my_globals, ldict)

        except SyntaxError as e:
            logger.log_error(f"The formula can not be executed. {e}")

        return _xr.DataArray(ldict["output"])

    def _safe_import(self, name, *args, **kwargs):
        # Redefine import, to only import from safe modules
        if name not in self._SAFE_MODULES:
            raise _ArgumentError(None, f"Importing {name!r} is not allowed!")
        return __import__(name, *args, **kwargs)
