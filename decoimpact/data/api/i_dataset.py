# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the 
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
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
    def start_date(self) -> str:
        """start date to filter the dataset"""
        # start_date is passed as string (not datetime) because it is optional

    @property
    @abstractmethod
    def end_date(self) -> str:
        """end date to filter the dataset"""
        # end_date is passed as string (not datetime) because it is optional

    @property
    @abstractmethod
    def mapping(self) -> dict[str, str]:
        """Variable name mapping (source to target)"""
