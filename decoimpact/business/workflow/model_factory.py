"""
Module for ModelFactory class

Classes:
    ModelFactory

"""


from decoimpact.business.entities.rule_based_model import RuleBasedModel
from decoimpact.crosscutting.logger import Logger


class ModelFactory:
    """Factory for creating models"""

    @ staticmethod
    def create_rule_based_model(logger: Logger) -> RuleBasedModel:
        """Creates an RuleBasedModel

        Returns:
            RuleBasedModel: instance of a RuleBasedModel
        """

        logger.log_info("Creating rule-based model")

        return RuleBasedModel()
