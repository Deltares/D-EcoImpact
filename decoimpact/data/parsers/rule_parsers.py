"""
Module for available list of RuleParsers

Classes:
    RuleParsers
"""
from typing import List

from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.parser_multiply_rule import ParserMultiplyRule
from decoimpact.data.parsers.parser_time_aggregation_rule import (
    ParserTimeAggregationRule,
)


def rule_parsers() -> List[IParserRuleBase]:
    """Function to return rule parsers"""
    return [ParserMultiplyRule(), ParserTimeAggregationRule()]
