"""
Module for IDataAccessLayer interface

Interfaces:
    IDataAccessLayer

"""

from abc import ABC, abstractmethod

from decoimpact.data.api.i_model_data import IModelData


class IDataAccessLayer(ABC):
    """Interface for the data layer"""

    @abstractmethod
    def read_input_file(self, path: str) -> IModelData:
        """Reads input file from provided path

        Args:
            path (str): path to input file

        Returns:
            IModelData: Data regarding model
        """
