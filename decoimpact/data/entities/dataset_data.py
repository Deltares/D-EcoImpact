"""
Module for DatasetData interface

Classes:
    DatasetData

"""

from typing import Any

from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.dictionary_utils import get_dict_element as _get_dict_element


class DatasetData(IDatasetData):
    """Class for storing dataset information"""

    def __init__(self, dataset: dict[str, Any]):
        """Create DatasetData based on provided info dictionary

        Args:
            info (dict[str, Any]):
        """
        super()
        self._path = _get_dict_element("filename", dataset)
        self._mapping = _get_dict_element("variable_mapping", dataset, False)

    @property
    def path(self) -> str:
        """File path to the dataset"""
        return self._path

    @property
    def mapping(self) -> dict[str, str]:
        """Variable name mapping (source to target)"""
        return self._mapping
