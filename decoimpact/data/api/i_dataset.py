"""
Module for IDatasetData interface

Interfaces:
    IDatasetData

"""

from abc import ABC, abstractmethod
from pathlib import Path


class IDatasetData(ABC):
    """Interface for dataset information"""

    @property
    @abstractmethod
    def path(self) -> Path:
        """File path to the dataset"""

    @property
    @abstractmethod
    def mappings(self) -> dict[str, str]:
        """Variable name mappings (source to target)"""
