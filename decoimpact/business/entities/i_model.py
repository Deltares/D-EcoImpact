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

    def __init__(self) -> None:
        self._status = ModelStatus.CREATED

    @property
    def name(self) -> str:
        """Name of the model"""
        return self._name

    @name.setter
    def name(self, name: str):
        """Name of the model"""
        self._name = name

    @property
    def status(self) -> ModelStatus:
        """Status of the model"""
        return self._status

    @status.setter
    def status(self, status: ModelStatus):
        """Status of the model"""
        self._status = status

    @property
    @abstractmethod
    def input_datasets(self) -> List[_xr.Dataset]:
        """Status of the model"""

    @abstractmethod
    def validate(self) -> bool:
        """Validates the model"""

    @abstractmethod
    def initialize(self) -> None:
        """Initializes the model"""

    @abstractmethod
    def execute(self) -> None:
        """Executes the model"""

    @abstractmethod
    def finalize(self) -> None:
        """Finalizes the model"""
