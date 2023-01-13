
"""
Module for ModelBase class

Classes:
    ModelBase

"""
from abc import ABC, abstractmethod
from enum import IntEnum


class ModelStatus(IntEnum):
    """Enum for the model status"""
    CREATED = 1,
    INITIALIZING = 2,
    INITIALIZED = 3,
    EXECUTING = 4,
    EXECUTED = 5,
    FINALIZING = 6,
    FINALIZED = 7,
    FAILED = 8,
    VALIDATING = 9,
    VALIDATED = 10


class ModelBase(ABC):
    """Base class for models"""

    def __init__(self) -> None:
        self._status = ModelStatus.CREATED

    @property
    def rules(self) -> ModelStatus:
        """Status of the model"""
        return self._status

    @rules.setter
    def rules(self, status: ModelStatus):
        """Status of the model"""
        self._status = status

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
