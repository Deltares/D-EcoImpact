# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the 
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for IModel Interface

Interfaces:
    IModel

Classes:
    ModelStatus

"""

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List

import xarray as _xr

from decoimpact.crosscutting.i_logger import ILogger


class ModelStatus(Enum):
    """Enum for the model status"""

    CREATED = auto()
    INITIALIZING = auto()
    INITIALIZED = auto()
    EXECUTING = auto()
    EXECUTED = auto()
    FINALIZING = auto()
    FINALIZED = auto()
    FAILED = auto()
    VALIDATING = auto()
    VALIDATED = auto()


class IModel(ABC):
    """Interface for models"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the model"""

    @property
    @abstractmethod
    def status(self) -> ModelStatus:
        """Status of the model"""

    @status.setter
    @abstractmethod
    def status(self, status: ModelStatus):
        """Status of the model"""

    @property
    @abstractmethod
    def input_datasets(self) -> List[_xr.Dataset]:
        """Input datasets for the model"""

    @property
    @abstractmethod
    def output_dataset(self) -> _xr.Dataset:
        """Output dataset produced by this model"""

    @abstractmethod
    def validate(self, logger: ILogger) -> bool:
        """Validates the model"""

    @abstractmethod
    def initialize(self, logger: ILogger) -> None:
        """Initializes the model"""

    @abstractmethod
    def execute(self, logger: ILogger) -> None:
        """Executes the model"""

    @abstractmethod
    def finalize(self, logger: ILogger) -> None:
        """Finalizes the model"""
