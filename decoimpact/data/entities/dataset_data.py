"""
Module for DatasetData interface

Classes:
    DatasetData

"""

from pathlib import Path
from typing import Any

from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.dictionary_utils import get_dict_element


class DatasetData(IDatasetData):
    """Class for storing dataset information"""

    def __init__(self, dataset: dict[str, Any]):
        """Create DatasetData based on provided info dictionary

        Args:
            dataset (dict[str, Any]):
        """
        super()
        self._path = Path(get_dict_element("filename", dataset)).resolve()
        self._get_mapping(dataset)

    @property
    def path(self) -> Path:
        """File path to the input dataset"""
        return self._path

    @property
    def mapping(self) -> dict[str, str]:
        """Variable name mapping (source to target)"""
        return self._mapping

    def _get_mapping(self, dataset: dict[str, Any]):
        """Get mapping specified in input file

        Args:
            dataset (dict[str, Any]):
        """
        self._mapping = get_dict_element("variable_mapping", dataset, False)
