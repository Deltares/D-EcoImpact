"""
Module for IDatasetData interface

Interfaces:
    IDatasetData

"""

from abc import ABC, abstractmethod
import xarray as _xr


class IDatasetData(ABC):
    """Interface for dataset information"""

    def __init__(self):
        pass

    @property
    @abstractmethod
    def path(self) -> str:
        """File path to the dataset"""

    @property
    @abstractmethod
    def mapping(self) -> dict[str, str]:
        """Variable name mapping (source to target)"""

    @abstractmethod
    def get_input_dataset(self) -> _xr.Dataset:
        """Read the dataset using the specified path"""
