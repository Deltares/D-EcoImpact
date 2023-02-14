"""
Module for Application class

Classes:
    Application

"""


from pathlib import Path
from typing import Callable

from decoimpact.business.entities.i_model import IModel
from decoimpact.business.workflow.model_runner import ModelRunner
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_data_access_layer import IDataAccessLayer

# only import interfaces to stay loosely coupled
from decoimpact.data.api.i_model_data import IModelData


class Application:
    """Application for running command-line"""

    def __init__(
        self,
        logger: ILogger,
        da_layer: IDataAccessLayer,
        model_creator: Callable[[ILogger, IModelData], IModel],
    ):
        """Creates an application based on provided logger, data-access layer
        and model creator function (optional)

        Args:
            logger (ILogger): Logger that takes care of logging
            da_layer (IDataAccessLayer): data-access layer for reading/writing
            data model_creator (Callable[[ILogger, IModelData], IModel]):
            Function for creating a model based on IModelData.
        """

        self._logger = logger
        self._da_layer = da_layer
        self._model_creator = model_creator

    def run(self, input_path: str, output_path: Path):
        """Runs application

        Args:
            input_path (str): path to input file
            output_path (str): path to output files
        """

        model_data: IModelData = self._da_layer.read_input_file(input_path)
        model: IModel = self._model_creator(self._logger, model_data)

        ModelRunner.run_model(model, self._logger)

        self._da_layer.write_output_files(model.output_dataset, output_path)
