"""
Module for DataAccessLayer class

Classes:
    DataAccessLayer

"""

import os as _os
from pathlib import Path
from typing import Any

import ruamel.yaml as _yaml

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_data_access_layer import IDataAccessLayer
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.entities.model_data_builder import ModelDataBuilder


class DataAccessLayer(IDataAccessLayer):
    """Implementation of the data layer"""

    def __init__(self, logger: ILogger):
        self._logger = logger

    def read_input_file(self, path: str) -> IModelData:
        """Reads input file from provided path

        Args:
            path (str): path to input file

        Returns:
            IModelData: Data regarding model

        Raises:
            FileExistsError: if file does not exist
        """
        self._logger.log_info(f"Creating model data based on yaml file {path}")

        if not _os.path.exists(path):
            raise FileExistsError(f"The input file {path} does not exist.")

        with open(path, "r", encoding="utf-8") as stream:
            contents: dict[Any, Any] = _yaml.load(stream, Loader=_yaml.Loader)
            model_data_builder = ModelDataBuilder()
            return model_data_builder.parse_yaml_data(contents)

    def write_output_file(self, path: Path) -> None:
        """Write XArray dataset to specified path

        Args:
            path (str): path to input file"""
        if not Path.exists(path.parent):
            message = f"""The path {path.parent} is not found. \
                          Make sure the outputfile location is valid."""
            raise FileExistsError(message)

        if Path(path).suffix != ".nc":
            message = f"""The file {path} is not supported. \
                          Currently only UGrid (NetCDF) files are supported."""
            raise NotImplementedError(message)

        try:
            self.to_netcdf(path, format="NETCDF4")
            # D-Flow FM sometimes still uses netCDF3.
            # If necessary we can revert to "NETCDF4_CLASSIC"
            # (Data is stored in an HDF5 file, using only netCDF 3 compatible
            # API features.)

        except OSError as exc:
            msg = "ERROR: Cannot write output .nc file -- " + str(path)
            raise OSError(msg) from exc

        return path
