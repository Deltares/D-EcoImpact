"""
Module for ModelBuilder class

Classes:
    ModelBuilder

"""

from typing import Iterable, List

from decoimpact.business.entities.i_model import IModel
from decoimpact.business.entities.rule_based_model import RuleBasedModel
from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.business.entities.rules.multiply_rule import MultiplyRule
from decoimpact.business.entities.rules.time_aggregation_rule import TimeAggregationRule
from decoimpact.business.workflow.i_model_builder import IModelBuilder
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_data_access_layer import IDataAccessLayer
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.api.i_multiply_rule_data import IMultiplyRuleData
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.api.i_time_aggregation_rule_data import ITimeAggregationRuleData


class ModelBuilder(IModelBuilder):
    """Factory for creating models"""

    def __init__(self, da_layer: IDataAccessLayer, logger: ILogger) -> None:
        self._logger = logger
        self._da_layer = da_layer

    def build_model(self, model_data: IModelData) -> IModel:
        """Creates an model based on model data

        Returns:
            IModel: instance of a model based on model data
        """

        self._logger.log_info("Creating rule-based model")

        datasets = [self._da_layer.read_input_dataset(ds) for ds in model_data.datasets]
        rules = list(ModelBuilder._create_rules(model_data.rules))

        model: IModel = RuleBasedModel(datasets, rules, model_data.name)

        return model

    @staticmethod
    def _create_rules(rule_data: List[IRuleData]) -> Iterable[IRule]:
        for rule_data_object in rule_data:
            yield ModelBuilder._create_rule(rule_data_object)

    @staticmethod
    def _create_rule(rule_data: IRuleData) -> IRule:

        if isinstance(rule_data, IMultiplyRuleData):
            return MultiplyRule(
                rule_data.name,
                [rule_data.input_variable],
                rule_data.multipliers,
                rule_data.output_variable,
            )
        elif isinstance(rule_data, ITimeAggregationRuleData):
            return TimeAggregationRule(
                rule_data.name,
                [rule_data.input_variable],
                rule_data.operation,
                rule_data.output_variable,
                rule_data.time_scale,
            )

        error_str = (
            f"The rule type of rule '{rule_data.name}' is currently " "not implemented"
        )
        raise NotImplementedError(error_str)
