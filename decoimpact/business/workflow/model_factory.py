"""
Module for ModelFactory class

Classes:
    ModelFactory

"""


from typing import Iterable, List

from decoimpact.business.entities.i_model import IModel
from decoimpact.business.entities.rule_based_model import RuleBasedModel
from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.business.entities.rules.multiply_rule import MultiplyRule
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.api.i_multiply_rule_data import IMultiplyRuleData
from decoimpact.data.api.i_rule_data import IRuleData


class ModelFactory:
    """Factory for creating models"""

    @staticmethod
    def create_model(logger: ILogger, model_data: IModelData) -> IModel:
        """Creates an RuleBasedModel

        Returns:
            RuleBasedModel: instance of a RuleBasedModel
        """

        logger.log_info("Creating rule-based model")

        datasets = [ds.get_input_dataset() for ds in model_data.datasets]
        rules = list(ModelFactory._create_rules(model_data.rules))

        model: IModel = RuleBasedModel(datasets, rules, model_data.name)

        return model

    @staticmethod
    def _create_rules(rule_data: List[IRuleData]) -> Iterable[IRule]:
        for rule_data_object in rule_data:
            yield ModelFactory._create_rule(rule_data_object)

    @staticmethod
    def _create_rule(rule_data: IRuleData) -> IRule:

        if isinstance(rule_data, IMultiplyRuleData):
            return MultiplyRule(
                rule_data.name,
                [rule_data.input_variable],
                rule_data.multipliers,
                rule_data.output_variable)

        raise NotImplementedError(f"The rule type of rule '{rule_data.name}' is currently not implemented")

