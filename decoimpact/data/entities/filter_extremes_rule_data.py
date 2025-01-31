# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for FilterExtremesRuleData class

Classes:
    FilterExtremesRuleData

"""

from typing import List

from decoimpact.data.api.i_filter_extremes_rule_data import IFilterExtremesRuleData
from decoimpact.data.entities.rule_data import RuleData


class FilterExtremesRuleData(IFilterExtremesRuleData, RuleData):
    """Class for storing data related to filter extremes rule"""

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    def __init__(
        self,
        name: str,
        input_variables: List[str],
        extreme_type: str,
        distance: int,
        time_scale: str,
        mask: bool,
    ):
        super().__init__(name)
        self._input_variables = input_variables
        self._extreme_type = extreme_type
        self._distance = distance
        self._time_scale = time_scale
        self._mask = mask

    @property
    def input_variables(self) -> List[str]:
        """List with input variables"""
        return self._input_variables

    @property
    def extreme_type(self) -> str:
        """Property for the extremes type"""
        return self._extreme_type

    @property
    def distance(self) -> int:
        """Property for the distance between peaks"""
        return self._distance

    @property
    def time_scale(self) -> str:
        """Property for the timescale of the distance between peaks"""
        return self._time_scale

    @property
    def mask(self) -> bool:
        """Property for mask"""
        return self._mask
