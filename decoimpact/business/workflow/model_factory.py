"""
Module for ModelFactory class

Classes:
    ModelFactory

"""


from typing import List

from decoimpact.business.entities.i_model import IModel
from decoimpact.business.entities.rule_based_model import RuleBasedModel
from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.rule_parsers import rule_parsers


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
        rules = ModelFactory._create_rules(model_data.rules)

        model: IModel = RuleBasedModel(datasets, rules, model_data.name)

        return model

    @staticmethod
    def _create_rules(rule_data: List[IRuleData]) -> List[IRule]:
        rules = []
        for rule_data_object in rule_data:
            parser = ModelFactory._get_parser(rule_data_object.name)
            rules.append(parser.parse_dict(rule_data_object.data))
        return rules

    @staticmethod
    def _get_parser(rule_name: str) -> IParserRuleBase:
        for parser in rule_parsers():
            if parser.rule_type_name == rule_name:
                return parser
        raise Exception(f"No parser for {rule_name}")
