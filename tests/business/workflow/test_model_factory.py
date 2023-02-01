"""
Tests for ModelFactory class
"""


from unittest.mock import Mock
from decoimpact.business.entities.rule_based_model import RuleBasedModel
from decoimpact.business.workflow.model_factory import ModelFactory
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.api.i_model_data import IModelData


def test_create_rule_based_model():
    """Test creating a rule-based model via factory"""

    # Arrange
    logger = Mock(ILogger)
    model_data = Mock(IModelData)
    dataset = Mock()
    dataset_data = Mock(IDatasetData)

    model_data.name = "Test model"
    model_data.datasets = [dataset_data]

    dataset_data.get_input_dataset.return_value = dataset

    # Act
    model = ModelFactory.create_model(logger, model_data)

    # Assert

    assert isinstance(model, RuleBasedModel)
    assert model.name == "Test model"
    assert dataset in model.input_datasets

    # logs info about model creation
    logger.log_info.assert_called_once()
