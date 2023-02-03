"""
Module for DatasetData interface

Classes:
    DatasetData

"""

from pathlib import Path
from typing import Any

import xarray as _xr

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
        self._path = Path(_get_dict_element("filename", dataset)).resolve()
        self._mapping = _get_dict_element("variable_mapping", dataset, False)

    @property
    def path(self) -> str:
        """File path to the dataset"""
        return self._path

    @property
    def mapping(self) -> dict[str, str]:
        """Variable name mapping (source to target)"""
        return self._mapping

    def get_input_dataset(self) -> _xr.Dataset:
        """XArray dataset for read from the specified path"""

        return self._get_original_dataset()

    def _get_original_dataset(self) -> _xr.Dataset:
        if not Path.exists(self._path):
            message = f"""The file {self._path} is not found. \
                          Make sure the file location is valid."""
            raise FileExistsError(message)
        if Path(self._path).suffix != ".nc":
            message = f"""The file {self._path} is not supported. \
                          Currently only UGrid (NetCDF) files are supported."""
            raise NotImplementedError(message)

        try:
            dataset: _xr.Dataset = _xr.open_dataset(self._path, mask_and_scale=True)
            # mask_and_scale argument is needed to prevent inclusion of NaN's in
            # dataset for missing values. This inclusion converts integers to
            # floats
        except OSError as exc:
            msg = "ERROR: Cannot open input .nc file -- " + str(self._path)
            raise OSError(msg) from exc

        return dataset
