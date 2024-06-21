# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
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
from decoimpact.business.entities.rules.axis_filter_rule import AxisFilterRule
from decoimpact.business.entities.rules.classification_rule import ClassificationRule
from decoimpact.business.entities.rules.combine_results_rule import CombineResultsRule
from decoimpact.business.entities.rules.depth_average_rule import DepthAverageRule
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
from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.business.entities.rules.step_function_rule import StepFunctionRule
from decoimpact.business.entities.rules.time_aggregation_rule import TimeAggregationRule
from decoimpact.business.workflow.i_model_builder import IModelBuilder
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_axis_filter_rule_data import IAxisFilterRuleData
from decoimpact.data.api.i_classification_rule_data import IClassificationRuleData
from decoimpact.data.api.i_combine_results_rule_data import ICombineResultsRuleData
from decoimpact.data.api.i_data_access_layer import IDataAccessLayer
from decoimpact.data.api.i_depth_average_rule_data import IDepthAverageRuleData
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
    def _set_default_fields(rule_data: IRuleData, rule: RuleBase):
        rule.description = rule_data.description
        rule.output_variable_name = rule_data.output_variable

    @staticmethod
    def _create_rule(rule_data: IRuleData) -> IRule:
        if isinstance(rule_data, IMultiplyRuleData):
            rule = MultiplyRule(
                rule_data.name,
                [rule_data.input_variable],
                rule_data.multipliers,
                rule_data.date_range,
            )
        elif isinstance(rule_data, IDepthAverageRuleData):
            rule = DepthAverageRule(
                rule_data.name,
                [rule_data.input_variable],
            )
        elif isinstance(rule_data, ILayerFilterRuleData):
            rule = LayerFilterRule(
                rule_data.name,
                [rule_data.input_variable],
                rule_data.layer_number,
            )
        elif isinstance(rule_data, IAxisFilterRuleData):
            rule = AxisFilterRule(
                rule_data.name,
                [rule_data.input_variable],
                rule_data.element_index,
                rule_data.axis_name,
            )
        elif isinstance(rule_data, IStepFunctionRuleData):
            rule = StepFunctionRule(
                rule_data.name,
                rule_data.input_variable,
                rule_data.limits,
                rule_data.responses,
            )
        elif isinstance(rule_data, ITimeAggregationRuleData):
            rule = TimeAggregationRule(
                rule_data.name, [rule_data.input_variable], rule_data.operation
            )
            rule.settings.percentile_value = rule_data.percentile_value
            rule.settings.time_scale = rule_data.time_scale
        elif isinstance(rule_data, IRollingStatisticsRuleData):
            rule = RollingStatisticsRule(
                rule_data.name, [rule_data.input_variable], rule_data.operation
            )
            rule.settings.percentile_value = rule_data.percentile_value
            rule.settings.time_scale = rule_data.time_scale
            rule.period = rule_data.period
        elif isinstance(rule_data, ICombineResultsRuleData):
            rule = CombineResultsRule(
                rule_data.name,
                rule_data.input_variable_names,
                MultiArrayOperationType[rule_data.operation_type],
            )
        elif isinstance(rule_data, IResponseCurveRuleData):
            rule = ResponseCurveRule(
                rule_data.name,
                rule_data.input_variable,
                rule_data.input_values,
                rule_data.output_values,
            )
        elif isinstance(rule_data, IFormulaRuleData):
            rule = FormulaRule(
                rule_data.name,
                rule_data.input_variable_names,
                rule_data.formula,
            )
        elif isinstance(rule_data, IClassificationRuleData):
            rule = ClassificationRule(
                rule_data.name, rule_data.input_variable_names, rule_data.criteria_table
            )
        elif isinstance(rule_data, IDepthAverageRuleData):
            rule = DepthAverageRule(
                rule_data.name, rule_data.input_variable, rule_data.output_variable
            )
        else:
            error_str = (
                f"The rule type of rule '{rule_data.name}' is currently "
                "not implemented"
            )
            raise NotImplementedError(error_str)

        if isinstance(rule, RuleBase):
            ModelBuilder._set_default_fields(rule_data, rule)

        return rule
