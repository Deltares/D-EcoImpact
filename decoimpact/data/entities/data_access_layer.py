"""
Module for DataAccessLayer class

Classes:
    DataAccessLayer

"""

from pathlib import Path
from typing import Any

import ruamel.yaml as _yaml
import xarray as _xr

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_data_access_layer import IDataAccessLayer
from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.entities.model_data_builder import ModelDataBuilder


class DataAccessLayer(IDataAccessLayer):
    """Implementation of the data layer"""

    def __init__(self, logger: ILogger):
        self._logger = logger

    def read_input_file(self, path: Path) -> IModelData:
        """Reads input file from provided path

        Args:
            path (str): path to input file

        Returns:
            IModelData: Data regarding model

        Raises:
            FileExistsError: if file does not exist
        """
        self._logger.log_info(f"Creating model data based on yaml file {path}")

        if not path.exists():
            msg = f"ERROR: The input file {path} does not exist."
            self._logger.log_error(msg)
            raise FileExistsError(msg)

        with open(path, "r", encoding="utf-8") as stream:
            contents: dict[Any, Any] = _yaml.load(stream, Loader=_yaml.Loader)
            model_data_builder = ModelDataBuilder()
            return model_data_builder.parse_yaml_data(contents)

    def read_input_dataset(self, dataset_data: IDatasetData) -> _xr.Dataset:
        """Uses the provided dataset_data to create/read a xarray Dataset

        Args:
            dataset_data (IDatasetData): dataset data for creating an
                                         xarray dataset

        Returns:
            _xr.Dataset: Dataset based on provided dataset_data
        """
        if not Path.exists(dataset_data.path):
            message = f"""The file {dataset_data.path} is not found. \
                          Make sure the input file location is valid."""
            raise FileExistsError(message)

        if dataset_data.path.suffix != ".nc":
            message = f"""The file {dataset_data.path} is not supported. \
                          Currently only UGrid (NetCDF) files are supported."""
            raise NotImplementedError(message)

        try:
            dataset: _xr.Dataset = _xr.open_dataset(dataset_data.path, mask_and_scale=True)
            # mask_and_scale argument is needed to prevent inclusion of NaN's
            # in dataset for missing values. This inclusion converts integers
            # to floats
        except ValueError as exc:
            msg = "ERROR: Cannot open input .nc file -- " + str(dataset_data.path)
            raise ValueError(msg) from exc

        return dataset

    def write_output_file(self, dataset: _xr.Dataset, path: Path) -> None:
        """Write XArray dataset to specified path

        Args:
            dataset (XArray dataset): dataset to write
            path (str): path to output file

        Returns:
            None

        Raises:
            FileExistsError: if output file location does not exist
            OSError: if output file cannot be written
        """
        self._logger.log_info(f"Writing model output data to {path}")

        if not Path.exists(path.parent):
            message = f"""The path {path.parent} is not found. \
                          Make sure the output file location is valid."""
            raise FileExistsError(message)

        if Path(path).suffix != ".nc":
            message = f"""The file {path} is not supported. \
                          Currently only UGrid (NetCDF) files are supported."""
            raise NotImplementedError(message)

        try:
            dataset.to_netcdf(path, format="NETCDF4")
            # D-Flow FM sometimes still uses netCDF3.
            # If necessary we can revert to "NETCDF4_CLASSIC"
            # (Data is stored in an HDF5 file, using only netCDF 3 compatible
            # API features.)

        except OSError as exc:
            msg = f"ERROR: Cannot write output .nc file -- {path}"
            self._logger.log_error(msg)
            raise OSError(msg) from exc

        return None
