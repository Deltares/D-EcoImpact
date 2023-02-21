"""
Module for IModelBuilder interface

InterfacesS:
    IModelBuilder

"""


from abc import ABC, abstractmethod

from decoimpact.business.entities.i_model import IModel
from decoimpact.data.api.i_model_data import IModelData


class IModelBuilder(ABC):
    """Factory for creating models"""

    @ abstractmethod
    def build_model(self, model_data: IModelData) -> IModel:
        """Creates an model based on model data

        Returns:
            IModel: instance of a model based on model data
        """
