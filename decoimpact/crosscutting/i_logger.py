# This file is part of D-EcoImpact
# Copyright (C) 2022-2023  Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the GNU
# Lesser General Public License version 2.1
# A copy of the GNU General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ILogger interface

Interfaces:
    ILogger

"""

from abc import ABC, abstractmethod


class ILogger(ABC):
    """Interface for a Logger"""

    @abstractmethod
    def log_error(self, message: str) -> None:
        """Logs an error message

        Args:
            message (str): message to log
        """

    @abstractmethod
    def log_warning(self, message: str) -> None:
        """Logs a warning message

        Args:
            message (str): message to log
        """

    @abstractmethod
    def log_info(self, message: str) -> None:
        """Logs a info message

        Args:
            message (str): message to log
        """

    @abstractmethod
    def log_debug(self, message: str) -> None:
        """Logs a debug message

        Args:
            message (str): message to log
        """
