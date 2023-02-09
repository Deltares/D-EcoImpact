"""
Tests for ModelFactory class
"""


from unittest.mock import Mock

from decoimpact.business.entities.rule_based_model import RuleBasedModel
from decoimpact.business.workflow.model_factory import ModelFactory
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.entities.multiply_rule_data import MultiplyRuleData


def test_create_rule_based_model():
    """Test creating a rule-based model via factory"""

    # Arrange
    logger = Mock(ILogger)
    model_data = Mock(IModelData)
    dataset = Mock()
    dataset_data = Mock(IDatasetData)

    rules_data = MultiplyRuleData("abc", [2,5.86], "a", "b")

    model_data.name = "Test model"
    model_data.datasets = [dataset_data]
    model_data.rules = [rules_data]

    dataset_data.get_input_dataset.return_value = dataset

    # Act
    model = ModelFactory.create_model(logger, model_data)

    # Assert

    assert isinstance(model, RuleBasedModel)
    assert model.name == "Test model"
    assert dataset in model.input_datasets
    assert len(model.rules) == 1

    # logs info about model creation
    logger.log_info.assert_called_once()
