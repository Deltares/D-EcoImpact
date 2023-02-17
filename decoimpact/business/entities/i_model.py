"""
Module for IModel Interface

Interfaces:
    IModel

Classes:
    ModelStatus

"""

from abc import ABC, abstractmethod
from enum import IntEnum
from typing import List

import xarray as _xr

from decoimpact.crosscutting.i_logger import ILogger


class ModelStatus(IntEnum):
    """Enum for the model status"""
    CREATED = 1
    INITIALIZING = 2
    INITIALIZED = 3
    EXECUTING = 4
    EXECUTED = 5
    FINALIZING = 6
    FINALIZED = 7
    FAILED = 8
    VALIDATING = 9
    VALIDATED = 10


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
