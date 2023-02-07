"""
Module for IRuleData interface

Interfaces:
    IRuleData

"""

from abc import ABC, abstractmethod

import xarray as _xr


class IRuleData(ABC):
    """Interface for dataset information"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the rule"""

    @abstractmethod
    def get_input_variables(self) -> _xr.Dataset:
        """Read the rule using the name"""
