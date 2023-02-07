"""
Module for ModelFactory class

Classes:
    ModelFactory

"""


from decoimpact.business.entities.i_model import IModel
from decoimpact.business.entities.rule_based_model import RuleBasedModel
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.entities.data_access_layer import IModelData


class ModelFactory:
    """Factory for creating models"""

    @staticmethod
    def create_model(logger: ILogger, model_data: IModelData) -> IModel:
        """Creates an RuleBasedModel

        Returns:
            RuleBasedModel: instance of a RuleBasedModel
        """

        logger.log_info("Creating rule-based model")
        print("create model", model_data)

        datasets = [ds.get_input_dataset() for ds in model_data.datasets]
        rules = model_data.rules

        model: IModel = RuleBasedModel(datasets, rules, model_data.name)

        return model
