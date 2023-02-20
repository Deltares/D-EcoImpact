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
    def mapping(self) -> dict[str, str]:
        """Variable name mapping (source to target)"""
