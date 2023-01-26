"""
Tests for Application class
"""


from unittest.mock import Mock
from decoimpact.business.application import Application


def test_running_application():
    """Test creating a rule-based model via factory"""

    # Arrange
    logger = Mock()
    data_layer = Mock()
    model_data = Mock()

    model_data.name = "Test model"
    data_layer.read_input_file.return_value = model_data

    application = Application(logger, data_layer)

    # Act
    application.run("Test.yaml")

    # Assert
    expected_message = "Model \"Test model\" has successfully finished running"
    logger.log_info.assert_called_with(expected_message)
