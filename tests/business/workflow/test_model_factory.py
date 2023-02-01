"""
Tests for ModelFactory class
"""


from unittest.mock import Mock
from decoimpact.business.entities.rule_based_model import RuleBasedModel
from decoimpact.business.workflow.model_factory import ModelFactory


def test_create_rule_based_model():
    """Test creating a rule-based model via factory"""

    # Arrange
    logger = Mock()
    model_data = Mock()
    dataset = Mock()
    dataset_data = Mock()

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
