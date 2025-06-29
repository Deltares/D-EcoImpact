# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for DataAccessLayer class

Classes:
    DataAccessLayer

"""

import re
from datetime import datetime
from pathlib import Path
from typing import Any

import xarray as _xr
import yaml as _yaml

from decoimpact.business.utils.dataset_utils import reduce_dataset_for_writing
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_data_access_layer import IDataAccessLayer
from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.api.output_file_settings import OutputFileSettings
from decoimpact.data.entities.model_data_builder import ModelDataBuilder


class DataAccessLayer(IDataAccessLayer):
    """Implementation of the data layer"""

    def __init__(self, logger: ILogger):
        self._logger = logger

    def retrieve_file_names(self, path: Path) -> dict:
        """
        Find all files according to the pattern in the path string
        If the user gives one filename, one file is returned. The user
        can give in a * in the filename and all files that correspond to
        that pattern will be retrieved.

        Args:
            path (str): path to input file (with * for generic part)

        Returns:
            List: List of strings with all files in folder according to pattern

        """
        name_list = list(path.parent.glob(path.name))
        # check if there is at least 1 file found.
        if len(name_list) == 0:
            message = f"""No files found for inputfilename {path.name}. \
                          Make sure the input file location is valid."""
            raise FileExistsError(message)

        names = {}
        for name in name_list:
            if "*" in path.name:
                part = re.findall(path.name.replace("*", "(.*)"), name.as_posix())
                names["_".join(part)] = name
            else:
                names[""] = name
        return names

    def read_input_file(self, path: Path) -> IModelData:
        """Reads input file from provided path

        Args:
            path (str): path to input file

        Returns:
            IModelData: Data regarding model

        Raises:
            FileExistsError: if file does not exist
            AttributeError: if yaml data is invalid
        """
        self._logger.log_info(f"Creating model data based on yaml file {path}")

        if not path.exists():
            msg = f"ERROR: The input file {path} does not exist."
            self._logger.log_error(msg)
            raise FileExistsError(msg)

        with open(path, "r", encoding="utf-8") as stream:
            contents: dict[Any, Any] = _yaml.load(
                stream, Loader=self.__create_yaml_loader()
            )
            model_data_builder = ModelDataBuilder(self._logger)
            try:
                yaml_data = model_data_builder.parse_yaml_data(contents)
            except AttributeError as exc:
                raise AttributeError(f"Error reading input file. {exc}") from exc
            return yaml_data

    def read_input_dataset(self, dataset_data: IDatasetData) -> _xr.Dataset:
        """Uses the provided dataset_data to create/read a xarray Dataset

        Args:
            dataset_data (IDatasetData): dataset data for creating an
                                         xarray dataset

        Returns:
            _xr.Dataset: Dataset based on provided dataset_data
        """
        # get start and end date from input file and convert to date format
        # if start or end date is not given, then use None to slice the data
        date_format = "%d-%m-%Y"
        filter_start_date = None
        ds_start_date = dataset_data.start_date
        if ds_start_date != "None":
            filter_start_date = datetime.strptime(ds_start_date, date_format)
        filter_end_date = None
        ds_end_date = dataset_data.end_date
        if ds_end_date != "None":
            filter_end_date = datetime.strptime(ds_end_date, date_format)

        if dataset_data.path.suffix != ".nc":
            message = f"""The file {dataset_data.path} is not supported. \
                          Currently only UGrid (NetCDF) files are supported."""
            raise NotImplementedError(message)

        # open input dataset (from .nc file)
        try:
            dataset: _xr.Dataset = _xr.open_dataset(
                dataset_data.path, mask_and_scale=True
            )
            # mask_and_scale argument is needed to prevent inclusion of NaN's
            # in dataset for missing values. This inclusion converts integers
            # to floats
        except ValueError as exc:
            msg = "ERROR: Cannot open input .nc file -- " + str(dataset_data.path)
            raise ValueError(msg) from exc

        # apply time filter on input dataset
        try:
            if filter_start_date is not None or filter_end_date is not None:
                time_filter = f"({filter_start_date}, {filter_end_date})"
                self._logger.log_info(f"Applying time filter {time_filter} on dataset")
                dataset = dataset.sel(time=slice(filter_start_date, filter_end_date))
        except ValueError as exc:
            msg = "ERROR: error applying time filter on dataset"
            raise ValueError(msg) from exc
        return dataset

    def write_output_file(
        self, dataset: _xr.Dataset, path: Path, settings: OutputFileSettings
    ) -> None:
        """Write XArray dataset to specified path

        Args:
            dataset (XArray dataset): dataset to write
            path (str): path to output file
            settings (OutputFileSettings): settings to use for saving output

        Returns:
            None

        Raises:
            FileExistsError: if output file location does not exist
            OSError: if output file cannot be written
        """
        self._logger.log_info(f"Writing model output data to {path}")

        if not Path.exists(path.parent):
            # try to make intermediate folders
            Path(path.parent).mkdir(parents=True, exist_ok=True)

            if not Path.exists(path.parent):
                message = f"""The path {path.parent} is not found. \
                            Make sure the output file location is valid."""
                raise FileExistsError(message)

        if Path(path).suffix != ".nc":
            message = f"""The file {path} is not supported. \
                          Currently only UGrid (NetCDF) files are supported."""
            raise NotImplementedError(message)

        try:
            dataset.attrs["Version"] = settings.application_version
            dataset.attrs["Generated by"] = settings.application_name

            if settings.variables_to_save and len(settings.variables_to_save) > 0:
                dataset = reduce_dataset_for_writing(
                    dataset, settings.variables_to_save, self._logger
                )

            dataset.to_netcdf(path, format="NETCDF4")
            # D-Flow FM sometimes still uses netCDF3.
            # If necessary we can revert to "NETCDF4_CLASSIC"
            # (Data is stored in an HDF5 file, using only netCDF 3 compatible
            # API features.)

            # TO DO: write application_version to output file as a global attribute
        except OSError as exc:
            msg = f"ERROR: Cannot write output .nc file -- {path}"
            self._logger.log_error(msg)
            raise OSError(msg) from exc

    def yaml_include_constructor(self, loader: _yaml.Loader, node: _yaml.Node) -> Any:
        """constructor function to make !include (referencedfile) possible"""

        file_path = Path(loader.name).parent
        file_path = file_path.joinpath(loader.construct_yaml_str(node)).resolve()
        with open(file=file_path, mode="r", encoding="utf-8") as incl_file:
            return _yaml.load(incl_file, type(loader))

    def __create_yaml_loader(self):
        """create yaml loader"""

        loader = _yaml.FullLoader
        loader.add_constructor("!include", self.yaml_include_constructor)
        # Add support for scientific notation (example 1e5=100000)
        loader.add_implicit_resolver(
            "tag:yaml.org,2002:float",
            re.compile(
                """^(?:
            [-+]?(?:[0-9][0-9_]*)\\.[0-9_]*(?:[eE][-+]?[0-9]+)?
            |[-+]?(?:[0-9][0-9_]*)(?:[eE][-+]?[0-9]+)
            |\\.[0-9_]+(?:[eE][-+][0-9]+)?
            |[-+]?[0-9][0-9_]*(?::[0-5]?[0-9])+\\.[0-9_]*
            |[-+]?\\.(?:inf|Inf|INF)
            |\\.(?:nan|NaN|NAN))$""",
                re.X,
            ),
            list("-+0123456789."),
        )

        return loader
