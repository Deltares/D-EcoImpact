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
        self._inputpath = Path(get_dict_element("filename", dataset)).resolve()
        self._outputpath = Path(get_dict_element("outputfilename", dataset)).resolve()
        self._mapping = get_dict_element("variable_mapping", dataset, False)

    @property
    def inputpath(self) -> str:
        """File path to the input dataset"""
        return str(self._inputpath)

    @property
    def outputpath(self) -> str:
        """File path to the output dataset"""
        return str(self._outputpath)

    @property
    def mapping(self) -> dict[str, str]:
        """Variable name mapping (source to target)"""
        return self._mapping

    def get_input_dataset(self) -> _xr.Dataset:
        """XArray dataset for read from the specified path"""
        return self._get_original_dataset()

    def _get_original_dataset(self) -> _xr.Dataset:
        if not Path.exists(self._inputpath):
            message = f"""The file {self._inputpath} is not found. \
                          Make sure the inputfile location is valid."""
            raise FileExistsError(message)

        if Path(self._inputpath).suffix != ".nc":
            message = f"""The file {self._inputpath} is not supported. \
                          Currently only UGrid (NetCDF) files are supported."""
            raise NotImplementedError(message)

        try:
            dataset: _xr.Dataset = _xr.open_dataset(
                self._inputpath, mask_and_scale=True
            )
            # mask_and_scale argument is needed to prevent inclusion of NaN's
            # in dataset for missing values. This inclusion converts integers
            # to floats
        except ValueError as exc:
            msg = "ERROR: Cannot open input .nc file -- " + str(self._inputpath)
            raise ValueError(msg) from exc

        return dataset

    def write_output_file(self) -> _xr.Dataset:
        """Write XArray dataset to specified path"""
        return self._write_output_file()

    def _write_output_file(self) -> _xr.Dataset:
        if not Path.exists(self._outputpath.parent):
            message = f"""The path {self._outputpath.parent} is not found. \
                          Make sure the outputfile location is valid."""
            raise FileExistsError(message)

        if Path(self._outputpath).suffix != ".nc":
            message = f"""The file {self._outputpath} is not supported. \
                          Currently only UGrid (NetCDF) files are supported."""
            raise NotImplementedError(message)

        try:
            self.to_netcdf(self._outputpath, format="NETCDF4")
            # D-Flow FM sometimes still uses netCDF3.
            # If necessary we can revert to "NETCDF4_CLASSIC"
            # (Data is stored in an HDF5 file, using only netCDF 3 compatible
            # API features.)

        except OSError as exc:
            msg = "ERROR: Cannot write output .nc file -- " + str(self._outputpath)
            raise OSError(msg) from exc

        return self
