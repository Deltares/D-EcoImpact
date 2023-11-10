# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ModelBuilder class

Classes:
    ModelBuilder

"""

from typing import Iterable, List

from decoimpact.business.entities.i_model import IModel
from decoimpact.business.entities.rule_based_model import RuleBasedModel
from decoimpact.business.entities.rules.classification_rule import ClassificationRule
from decoimpact.business.entities.rules.combine_results_rule import CombineResultsRule
from decoimpact.business.entities.rules.formula_rule import FormulaRule
from decoimpact.business.entities.rules.i_rule import IRule
from decoimpact.business.entities.rules.layer_filter_rule import LayerFilterRule
from decoimpact.business.entities.rules.multi_array_operation_type import (
    MultiArrayOperationType,
)
from decoimpact.business.entities.rules.multiply_rule import MultiplyRule
from decoimpact.business.entities.rules.response_curve_rule import ResponseCurveRule
from decoimpact.business.entities.rules.rolling_statistics_rule import (
    RollingStatisticsRule,
)
from decoimpact.business.entities.rules.step_function_rule import StepFunctionRule
from decoimpact.business.entities.rules.time_aggregation_rule import TimeAggregationRule
from decoimpact.business.workflow.i_model_builder import IModelBuilder
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_classification_rule_data import IClassificationRuleData
from decoimpact.data.api.i_combine_results_rule_data import ICombineResultsRuleData
from decoimpact.data.api.i_data_access_layer import IDataAccessLayer
from decoimpact.data.api.i_formula_rule_data import IFormulaRuleData
from decoimpact.data.api.i_layer_filter_rule_data import ILayerFilterRuleData
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.api.i_multiply_rule_data import IMultiplyRuleData
from decoimpact.data.api.i_response_curve_rule_data import IResponseCurveRuleData
from decoimpact.data.api.i_rolling_statistics_rule_data import (
    IRollingStatisticsRuleData,
)
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.api.i_step_function_rule_data import IStepFunctionRuleData
from decoimpact.data.api.i_time_aggregation_rule_data import ITimeAggregationRuleData


class ModelBuilder(IModelBuilder):
    """Factory for creating models"""

    def __init__(self, da_layer: IDataAccessLayer, logger: ILogger) -> None:
        self._logger = logger
        self._da_layer = da_layer

    def build_model(self, model_data: IModelData) -> IModel:
        """Creates a model based on model data.
        Current mapping works only for one dataset.

        Returns:
            IModel: instance of a model based on model data
        """

        self._logger.log_info("Creating rule-based model")

        datasets = [self._da_layer.read_input_dataset(ds) for ds in model_data.datasets]
        rules = list(ModelBuilder._create_rules(model_data.rules))

        mapping = model_data.datasets[0].mapping

        model: IModel = RuleBasedModel(datasets, rules, mapping, model_data.name)

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
                rule_data.date_range,
            )

        if isinstance(rule_data, ILayerFilterRuleData):
            return LayerFilterRule(
                rule_data.name,
                [rule_data.input_variable],
                rule_data.layer_number,
                rule_data.output_variable,
            )

        if isinstance(rule_data, IStepFunctionRuleData):
            return StepFunctionRule(
                rule_data.name,
                rule_data.input_variable,
                rule_data.limits,
                rule_data.responses,
                rule_data.output_variable,
            )

        if isinstance(rule_data, ITimeAggregationRuleData):
            return TimeAggregationRule(
                rule_data.name,
                [rule_data.input_variable],
                rule_data.operation,
                rule_data.operation_parameter,
                rule_data.output_variable,
                rule_data.time_scale,
            )
            
        if isinstance(rule_data, IRollingStatisticsRuleData):
            return RollingStatisticsRule(
                rule_data.name,
                [rule_data.input_variable],
                rule_data.operation,
                rule_data.operation_parameter,
                rule_data.output_variable,
                rule_data.time_scale,
                rule_data.period,
            )
            
        if isinstance(rule_data, ICombineResultsRuleData):
            return CombineResultsRule(
                rule_data.name,
                rule_data.input_variable_names,
                MultiArrayOperationType[rule_data.operation_type],
                rule_data.output_variable,
                rule_data.description,
            )
        if isinstance(rule_data, IResponseCurveRuleData):
            return ResponseCurveRule(
                rule_data.name,
                rule_data.input_variable,
                rule_data.input_values,
                rule_data.output_values,
                rule_data.output_variable,
                rule_data.description,
            )
        if isinstance(rule_data, IFormulaRuleData):
            return FormulaRule(
                rule_data.name,
                rule_data.input_variable_names,
                rule_data.formula,
                rule_data.output_variable,
                rule_data.description,
            )
        if isinstance(rule_data, IClassificationRuleData):
            return ClassificationRule(
                rule_data.name,
                rule_data.input_variable_names,
                rule_data.criteria_table,
                rule_data.output_variable,
                rule_data.description,
            )
        error_str = (
            f"The rule type of rule '{rule_data.name}' is currently " "not implemented"
        )
        raise NotImplementedError(error_str)
