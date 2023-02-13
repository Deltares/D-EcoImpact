"""
Tests for the ParserStepFunctionRule class
"""

from typing import Any, Dict

from decoimpact.business.entities.rules.rule_base import RuleBase
from decoimpact.business.entities.rules.step_function_rule import StepFunction
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.parser_step_function_rule import ParserStepFunctionRule
