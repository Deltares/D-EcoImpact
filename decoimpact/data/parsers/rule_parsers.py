"""
Module for available list of RuleParsers

Classes:
    RuleParsers
"""
from typing import Iterator

from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.parser_multiply_rule import ParserMultiplyRule
from decoimpact.data.parsers.parser_step_function_rule import ParserStepFunctionRule


def rule_parsers() -> Iterator[IParserRuleBase]:
    """Function to return rule parsers"""
    yield ParserMultiplyRule()
    yield ParserStepFunctionRule()
