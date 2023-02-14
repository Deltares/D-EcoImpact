"""
Tests for Application class
"""


from pathlib import Path
from unittest.mock import Mock

from decoimpact.business.application import Application
from decoimpact.business.entities.i_model import IModel
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_data_access_layer import IDataAccessLayer


def test_running_application():
    """Test running application for test file"""

    # Arrange
    logger = Mock(ILogger)
    data_layer = Mock(IDataAccessLayer)
    model: IModel = Mock(IModel)

    model.name = "Test model"

    application = Application(logger, data_layer, (lambda log, md: model))

    # Act
    application.run("Test.yaml", Path("./output.nc"))

    # Assert
    expected_message = 'Model "Test model" has successfully finished running'
    logger.log_info.assert_called_with(expected_message)

    model.validate.assert_called()
    model.initialize.assert_called()
    model.execute.assert_called()
    model.finalize.assert_called()
    # assert
