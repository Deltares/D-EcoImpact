"""
Module for IDataAccessLayer interface

Interfaces:
    IDataAccessLayer

"""

from abc import ABC, abstractmethod
from pathlib import Path

import xarray as _xr

from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.api.i_model_data import IModelData


class IDataAccessLayer(ABC):
    """Interface for the data layer"""

    @abstractmethod
    def read_input_file(self, path: Path) -> IModelData:
        """Reads input file from provided path

        Args:
            path (str): path to input file

        Returns:
            IModelData: Data regarding model
        """

    @abstractmethod
    def read_input_dataset(self, dataset_data: IDatasetData) -> _xr.Dataset:
        """Uses the provided dataset_data to create/read a xarray Dataset

        Args:
            dataset_data (IDatasetData): dataset data for creating an
                                         xarray dataset

        Returns:
            _xr.Dataset: Dataset based on provided dataset_data
        """

    @abstractmethod
    def write_output_file(self, dataset: _xr.Dataset, path: Path) -> None:
        """Write output files to provided path

        Args:
            dataset (XArray dataset): dataset to write
            path (str): path to output file

        Returns:
            None
        """
