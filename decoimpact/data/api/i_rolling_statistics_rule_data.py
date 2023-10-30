# This file is part of D-EcoImpact
# Copyright (C) 2022-2023  Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the GNU
# Lesser General Public License version 2.1
# A copy of the GNU General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for IRollingStatisticsRuleData interface

Interfaces:
    IRollingStatisticsRuleData

"""


from abc import ABC, abstractmethod

from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.api.time_operation_type import TimeOperationType


class IRollingStatisticsRuleData(IRuleData, ABC):
    """Data for a RollingStatisticsRule"""

    @property
    @abstractmethod
    def input_variable(self) -> str:
        """Name of the input variable"""

    @property
    @abstractmethod
    def operation(self) -> TimeOperationType:
        """Operation type"""
    
    @property
    @abstractmethod
    def operation_parameter(self) -> float:
        """Operation parameter"""

    @property
    @abstractmethod
    def time_scale(self) -> str:
        """Time scale"""

    @property
    @abstractmethod
    def period(self) -> float:
        """Period"""
