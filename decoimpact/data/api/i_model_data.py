"""
Module for IModelData interface

Interfaces:
    IModelData

"""

from abc import ABC, abstractmethod
from typing import List

from decoimpact.data.api.i_dataset import IDatasetData


class IModelData(ABC):
    """Interface for the model data"""

    def __init__(self):
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the model"""

    @property
    @abstractmethod
    def datasets(self) -> List[IDatasetData]:
        """Datasets of the model"""
