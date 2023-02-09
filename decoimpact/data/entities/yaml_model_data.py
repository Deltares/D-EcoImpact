"""
Module for YamlModelData class

Classes:
    YamlModelData

"""

from typing import List

from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.api.i_rule_data import IRuleData


class YamlModelData(IModelData):
    """Implementation of the model data"""

    def __init__(self, name: str, datasets: List[IDatasetData], rules: List[IRuleData]):
        super()
        self._name = name
        self._datasets = datasets
        self._rules = rules

    @property
    def name(self) -> str:
        """Name of the model"""
        return self._name

    @property
    def datasets(self) -> List[IDatasetData]:
        """Datasets of the model"""
        return self._datasets

    @property
    def rules(self) -> List[IRuleData]:
        """Rules of the model"""
        return self._rules
