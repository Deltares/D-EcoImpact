"""
Module for DatasetData interface

Classes:
    DatasetData

"""

from pathlib import Path
from typing import Any

import xarray as _xr

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
        self._mapping = get_dict_element("variable_mapping", dataset, False)

    @property
    def path(self) -> str:
        """File path to the dataset"""
        return str(self._path)

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
                          Make sure the inputfile location is valid."""
            raise FileExistsError(message)

        if Path(self._path).suffix != ".nc":
            message = f"""The file {self._path} is not supported. \
                          Currently only UGrid (NetCDF) files are supported."""
            raise NotImplementedError(message)

        try:
            dataset: _xr.Dataset = _xr.open_dataset(self._path, mask_and_scale=True)
            # mask_and_scale argument is needed to prevent inclusion of NaN's
            # in dataset for missing values. This inclusion converts integers
            # to floats
        except ValueError as exc:
            msg = "ERROR: Cannot open input .nc file -- " + str(self._path)
            raise ValueError(msg) from exc

        return dataset

    def write_output_file(self, output_path: Path) -> _xr.Dataset:
        """Write XArray dataset to specified path"""
        return self._write_output_file(output_path)

    def _write_output_file(self, output_path: Path) -> _xr.Dataset:
        if not Path.exists(output_path.parent):
            message = f"""The path {output_path.parent} is not found. \
                          Make sure the outputfile location is valid."""
            raise FileExistsError(message)

        if Path(output_path).suffix != ".nc":
            message = f"""The file {output_path} is not supported. \
                          Currently only UGrid (NetCDF) files are supported."""
            raise NotImplementedError(message)

        try:
            dataset: _xr.Dataset = _xr.Dataset.to_netcdf(output_path, format="NETCDF4")
            # D-Flow FM sometimes still uses netCDF3.
            # If necessary we can revert to "NETCDF4_CLASSIC"
            # (Data is stored in an HDF5 file, using only netCDF 3 compatible
            # API features.)

        except OSError as exc:
            msg = "ERROR: Cannot write output .nc file -- " + str(output_path)
            raise OSError(msg) from exc

        return dataset
