# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
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
        self._start_date = str(get_dict_element("start_date", dataset, False))
        self._end_date = str(get_dict_element("end_date", dataset, False))
        self._get_mapping(dataset)

    @property
    def path(self) -> Path:
        """File path to the input dataset"""
        return self._path

    @property
    def start_date(self) -> str:
        """optional start date to filter the dataset"""
        # start_date is passed as string (not datetime) because it is optional
        return self._start_date

    @property
    def end_date(self) -> str:
        """optional end date to filter the dataset"""
        # end_date is passed as string (not datetime) because it is optional
        return self._end_date

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
