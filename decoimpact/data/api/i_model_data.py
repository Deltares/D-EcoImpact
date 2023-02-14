"""
Module for IModelData interface

Interfaces:
    IModelData

"""

from abc import ABC, abstractmethod
from typing import List

import xarray as _xr

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
    def output_dataset(self) -> _xr.Dataset:
        """Model dataset to write to output file"""

    @property
    @abstractmethod
    def rules(self) -> List[IRuleData]:
        """Rules of the model"""
