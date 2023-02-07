"""
Module for YamlModelData class

Classes:
    YamlModelData

"""

from typing import Any, List

from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.entities.dataset_data import DatasetData


class YamlModelData(IModelData):
    """Implementation of the model data"""

    def __init__(self, name: str, yaml_contents: dict[str, Any]):
        super()
        self._name = name
        self._datasets: List[IDatasetData] = []

        self._parse_contents(yaml_contents)

    @property
    def name(self) -> str:
        """Name of the model"""
        return self._name

    @property
    def datasets(self) -> List[IDatasetData]:
        """Datasets of the model"""
        return self._datasets

    def _parse_contents(self, contents: dict[str, Any]):
        self._parse_datasets(contents)

    def _parse_datasets(self, contents: dict[str, Any]):
        datasets: List[dict[str, Any]] = get_dict_element("input-data", contents)

        for dataset in datasets:
            self._datasets.append(DatasetData(get_dict_element("dataset", dataset)))
