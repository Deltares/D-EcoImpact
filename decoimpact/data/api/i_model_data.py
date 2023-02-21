"""
Module for IModelData interface

Interfaces:
    IModelData

"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.api.i_rule_data import IRuleData


class IModelData(ABC):
    """Interface for the model data"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the model"""

    @property
    @abstractmethod
    def datasets(self) -> List[IDatasetData]:
        """Datasets of the model"""

    @abstractmethod
    def mappings(self) -> List[str]:
        """Mappings of datasets of the model"""

    @property
    @abstractmethod
    def output_path(self) -> Path:
        """Model path to the output file"""

    @property
    @abstractmethod
    def rules(self) -> List[IRuleData]:
        """Rules of the model"""
