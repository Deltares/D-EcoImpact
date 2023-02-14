"""
Module for IModelData interface

Interfaces:
    IModelData

"""

from abc import ABC, abstractmethod
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

    @property
    @abstractmethod
    def output_datasets(self) -> List[IDatasetData]:
        """Datasets of the model to write to output file"""

    @property
    @abstractmethod
    def rules(self) -> List[IRuleData]:
        """Rules of the model"""
