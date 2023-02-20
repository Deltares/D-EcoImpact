"""
Module for Application class

Classes:
    Application

"""


from pathlib import Path

from decoimpact.business.workflow.i_model_builder import IModelBuilder
from decoimpact.business.workflow.model_runner import ModelRunner

# only import interfaces to stay loosely coupled
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_data_access_layer import IDataAccessLayer
from decoimpact.data.api.i_model_data import IModelData


class Application:
    """Application for running command-line"""

    def __init__(
        self,
        logger: ILogger,
        da_layer: IDataAccessLayer,
        model_builder: IModelBuilder,
    ):
        """Creates an application based on provided logger, data-access layer
        and model builder

        Args:
            logger (ILogger): Logger that takes care of logging
            da_layer (IDataAccessLayer): data-access layer for reading/writing
            model_builder (IModelBuilder): builder for creating a model based on
            IModelData
        """
        self._logger = logger
        self._da_layer = da_layer
        self._model_builder = model_builder

    def run(self, input_path: Path):
        """Runs application

        Args:
            input_path (Path): path to input file
        """

        model_data: IModelData = self._da_layer.read_input_file(input_path)
        model = self._model_builder.build_model(model_data)

        ModelRunner.run_model(model, self._logger)

        self._da_layer.write_output_file(model.output_dataset, model_data.output_path)
