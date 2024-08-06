# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for IDataAccessLayer interface

Interfaces:
    IDataAccessLayer

"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

import xarray as _xr

from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.api.output_file_settings import OutputFileSettings


class IDataAccessLayer(ABC):
    """Interface for the data layer"""

    @abstractmethod
    def retrieve_partitioned_file_names(self, path: Path) -> List:
        """
        Find all files according to the pattern in the path string

        Args:
            path (str): path to input file (with * for generic part)

        Returns:
            List: List of strings with all files in folder according to pattern

        """

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
    def write_output_file(
        self, dataset: _xr.Dataset, path: Path, settings: OutputFileSettings
    ) -> None:
        """Write output files to provided path

        Args:
            dataset (XArray dataset): dataset to write
            path (str): path to output file
            settings (OutputFileSettings): settings to use for saving output

        Returns:
            None

        Raises:
            FileExistsError: if output file location does not exist
            OSError: if output file cannot be written
        """
