# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for Application class
"""


from unittest.mock import Mock

from decoimpact.business.application import Application
from decoimpact.business.entities.i_model import IModel
from decoimpact.business.workflow.i_model_builder import IModelBuilder
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_data_access_layer import IDataAccessLayer
from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.api.i_model_data import IModelData


def test_running_application():
    """Test running application for test file"""

    # Arrange
    logger = Mock(ILogger)
    data_layer = Mock(IDataAccessLayer)
    dataset = Mock(IDatasetData)
    model: IModel = Mock(IModel)
    model_builder = Mock(IModelBuilder)
    model_data = Mock(IModelData)

    model.name = "Test model"
    model.partition = ""
    model_builder.build_model.return_value = model
    data_layer.read_input_file.return_value = model_data
    data_layer.retrieve_file_names.return_value = {"": "Test.nc"}
    model_data.version = [0, 0, 0]
    model_data.datasets = [dataset]
    model_data.output_path = "Result_test.nc"

    application = Application(logger, data_layer, model_builder)
    application.APPLICATION_VERSION = "0.0.0"
    application.APPLICATION_VERSION_PARTS = [0, 0, 0]

    # Act
    application.run("Test.yaml")

    # Assert
    expected_message = 'Model "Test model" has successfully finished running'
    logger.log_info.assert_called_with(expected_message)

    model.validate.assert_called()
    model.initialize.assert_called()
    model.execute.assert_called()
    model.finalize.assert_called()
