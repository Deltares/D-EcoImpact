"""
Module for DataAccessLayer class

Classes:
    DataAccessLayer

"""

from typing import Any
import os as _os
import ruamel.yaml as _yaml

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_data_access_layer import IDataAccessLayer
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.entities.yaml_model_data import YamlModelData


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
            FileNotFoundError: if file does not exist
        """
        self._logger.log_info(f"Creating model data based on yaml file {path}")

        if not _os.path.exists(path):
            raise FileNotFoundError(f"The input file {path} does not exist.")

        with open(path, "r", encoding="utf-8") as stream:
            contents: dict[Any, Any] = _yaml.load(stream, Loader=_yaml.Loader)

            model_data = YamlModelData("Model 1", contents)

            return model_data
