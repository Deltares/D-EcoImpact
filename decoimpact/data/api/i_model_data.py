# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
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
    def version(self) -> List[int]:
        """Version of the model"""

    @property
    @abstractmethod
    def datasets(self) -> List[IDatasetData]:
        """Datasets of the model"""

    @property
    @abstractmethod
    def output_path(self) -> Path:
        """Model path to the output file"""

    @property
    @abstractmethod
    def output_variables(self) -> List[str]:
        """Output variables when a selection of output variables is made"""

    @property
    @abstractmethod
    def rules(self) -> List[IRuleData]:
        """Rules of the model"""
