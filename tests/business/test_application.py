"""
Tests for Application class
"""


from unittest.mock import MagicMock, Mock
from decoimpact.business.application import Application
from decoimpact.business.entities.i_model import IModel
from decoimpact.business.workflow.model_factory import ModelFactory
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_data_access_layer import IDataAccessLayer


def test_running_application():
    """Test running application for test file"""

    # Arrange
    logger = Mock(ILogger)
    data_layer = Mock(IDataAccessLayer)
    model: IModel = Mock(IModel)

    model.name = "Test model"

    # override create_model method to return mocked model
    ModelFactory.create_model = MagicMock(return_value=model)
    application = Application(logger, data_layer)

    # Act
    application.run("Test.yaml")

    # Assert
    expected_message = "Model \"Test model\" has successfully finished running"
    logger.log_info.assert_called_with(expected_message)

    model.validate.assert_called()
    model.initialize.assert_called()
    model.execute.assert_called()
    model.finalize.assert_called()
    # assert
