"""
Module for IModelData interface

Interfaces:
    IModelData

"""

from abc import ABC, abstractmethod


class IModelData(ABC):
    """Interface for the model data"""

    def __init__(self):
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the model"""
