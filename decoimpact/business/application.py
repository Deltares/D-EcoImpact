"""
Module for Application class

Classes:
    Application

"""


from decoimpact.crosscutting.i_logger import ILogger

# only import interfaces to stay loosely coupled
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.api.i_data_access_layer import IDataAccessLayer

from decoimpact.business.entities.i_model import IModel
from decoimpact.business.workflow.model_factory import ModelFactory
from decoimpact.business.workflow.model_runner import ModelRunner


class Application:
    """Application for running command-line"""

    def __init__(self, logger: ILogger, da_layer: IDataAccessLayer) -> None:
        self._logger = logger
        self._da_layer = da_layer

    def run(self, input_path: str):
        """Runs application

        Args:
            input_path (str): path to input file
        """

        model_data: IModelData = self._da_layer.read_input_file(input_path)
        model: IModel = ModelFactory.create_model(self._logger, model_data)

        ModelRunner.run_model(model, self._logger)
