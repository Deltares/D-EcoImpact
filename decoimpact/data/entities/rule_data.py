"""
Module for RuletData interface

Classes:
    RuletData

"""

from typing import Any

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import get_dict_element as _get_dict_element


class RuleData(IRuleData):
    """Class for storing rule information"""

    def __init__(self, rule: dict[str, Any]):
        """Create IRuleData based on provided info dictionary

        Args:
            info (dict[str, Any]):
        """
        super()
        self._mapping = _get_dict_element("variable_mapping", rule, False)

    # @property
    # def path(self) -> str:
    #     """File path to the dataset"""
    #     return str(self._path)

    # @property
    # def mapping(self) -> dict[str, str]:
    #     """Variable name mapping (source to target)"""
    #     return self._mapping
