"""
Module for RuletData interface

Classes:
    RuletData

"""

from typing import Any
import xarray as _xr

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import get_dict_element as _get_dict_element
from decoimpact.data.entities.rule_data import RuleData


class MultiplyRuleData(RuleData, IRuleData):
    """Class for storing and processing the information for the multiply rule"""

    def get_input_variables(self) -> _xr.Dataset:
