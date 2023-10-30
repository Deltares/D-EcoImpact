# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for available list of RuleParsers

Classes:
    RuleParsers
"""
from typing import Iterator

from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.parser_classification_rule import ParserClassificationRule
from decoimpact.data.parsers.parser_combine_results_rule import ParserCombineResultsRule
from decoimpact.data.parsers.parser_formula_rule import ParserFormulaRule
from decoimpact.data.parsers.parser_layer_filter_rule import ParserLayerFilterRule
from decoimpact.data.parsers.parser_multiply_rule import ParserMultiplyRule
from decoimpact.data.parsers.parser_response_curve_rule import ParserResponseCurveRule
from decoimpact.data.parsers.parser_rolling_statistics_rule import (
    ParserRollingStatisticsRule,
)
from decoimpact.data.parsers.parser_step_function_rule import ParserStepFunctionRule
from decoimpact.data.parsers.parser_time_aggregation_rule import (
    ParserTimeAggregationRule,
)


def rule_parsers() -> Iterator[IParserRuleBase]:
    """Function to return rule parsers"""
    yield ParserMultiplyRule()
    yield ParserCombineResultsRule()
    yield ParserLayerFilterRule()
    yield ParserTimeAggregationRule()
    yield ParserRollingStatisticsRule()
    yield ParserStepFunctionRule()
    yield ParserResponseCurveRule()
    yield ParserFormulaRule()
    yield ParserClassificationRule()
