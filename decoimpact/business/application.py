# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for Application class

Classes:
    Application

"""

from pathlib import Path

from decoimpact.business.entities.i_model import ModelStatus as _ModelStatus
from decoimpact.business.utils.version_utils import read_version_number
from decoimpact.business.workflow.i_model_builder import IModelBuilder
from decoimpact.business.workflow.model_runner import ModelRunner as _ModelRunner

# only import interfaces to stay loosely coupled
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_data_access_layer import IDataAccessLayer
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.api.output_file_settings import OutputFileSettings


class Application:
    """Application for running command-line"""

    # get version
    APPLICATION_VERSION = read_version_number()
    APPLICATION_NAME = "D-EcoImpact"
    # separate version into major, minor and patch:
    APPLICATION_VERSION_PARTS = list(map(int, APPLICATION_VERSION.split(".", 2)))

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

        try:
            # show application version
            self._logger.log_info(f"Application version: {self.APPLICATION_VERSION}")

            # read input file
            model_data: IModelData = self._da_layer.read_input_file(input_path)
            str_input_version = "".join([str(x) + "." for x in model_data.version])[:-1]
            self._logger.log_info(f"Input file version: {str_input_version}")

            # check version:
            message = (
                f"Application version {self.APPLICATION_VERSION} is older"
                " than version from input file {str_input_version}"
            )
            # major version (app) should be equal or larger then input version --> error
            if self.APPLICATION_VERSION_PARTS[0] < model_data.version[0]:
                self._logger.log_error(message)
            # minor version (app) should be equal or larger then input version --> warn
            elif self.APPLICATION_VERSION_PARTS[1] < model_data.version[1]:
                self._logger.log_warning(message)

            # build model
            for dataset in model_data.datasets:
                input_files = self._da_layer.retrieve_file_names(dataset.path)
                output_path_base = Path(model_data.output_path)
                for key, file_name in input_files.items():
                    dataset.path = file_name
                    output_path = self._generate_output_path(output_path_base, key)

                    model_data.partition = key
                    model = self._model_builder.build_model(model_data)

                    # run model
                    _ModelRunner.run_model(model, self._logger)

                    # write output file
                    if model.status == _ModelStatus.FINALIZED:
                        settings = OutputFileSettings(
                            self.APPLICATION_NAME, self.APPLICATION_VERSION
                        )
                        settings.variables_to_save = model_data.output_variables

                        self._da_layer.write_output_file(
                            model.output_dataset, output_path, settings
                        )

        except Exception as exc:  # pylint: disable=broad-except
            self._logger.log_error(f"Exiting application after error: {exc}")

    def _generate_output_path(self, output_path_base, key):
        if "*" in output_path_base.stem:
            output_path = Path(str(output_path_base).replace("*", key))
        else:
            partition_part = ""
            if key:
                partition_part = f"_{key}"
            output_path = Path.joinpath(
                output_path_base.parent,
                f"{output_path_base.stem}{partition_part}{output_path_base.suffix}",
            )
        return output_path
