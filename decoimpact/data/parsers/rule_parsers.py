"""
Module for available list of RuleParsers

Classes:
    RuleParsers
"""
from typing import Iterator

from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.parser_combine_results_rule import ParserCombineResultsRule
from decoimpact.data.parsers.parser_layer_filter_rule import ParserLayerFilterRule
from decoimpact.data.parsers.parser_multiply_rule import ParserMultiplyRule
from decoimpact.data.parsers.parser_time_aggregation_rule import (
    ParserTimeAggregationRule,
)


def rule_parsers() -> Iterator[IParserRuleBase]:
    """Function to return rule parsers"""
    yield ParserMultiplyRule()
    yield ParserCombineResultsRule()
    yield ParserLayerFilterRule()
    yield ParserTimeAggregationRule()
