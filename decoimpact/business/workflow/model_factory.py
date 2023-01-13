"""
Module for ModelFactory class

Classes:
    ModelFactory

"""


from decoimpact.business.entities.rule_based_model import RuleBasedModel


class ModelFactory:
    """Factory for creating models"""

    @ staticmethod
    def create_rule_based_model() -> RuleBasedModel:
        """Creates an RuleBasedModel

        Returns:
            RuleBasedModel: instance of a RuleBasedModel
        """
        return RuleBasedModel()
