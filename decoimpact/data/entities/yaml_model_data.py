"""
Module for YamlModelData class

Classes:
    YamlModelData

"""

from decoimpact.data.api.i_model_data import IModelData


class YamlModelData(IModelData):
    """Implementation of the model data"""

    def __init__(self):
        pass

    @property
    def name(self) -> str:
        """Name of the model"""
        return "Model 1"
