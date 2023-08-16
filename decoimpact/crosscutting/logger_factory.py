# This file is part of D-EcoImpact
# Copyright (C) 2022-2023  Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the GNU Lesser General Public
# A copy of the GNU General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for LoggerFactory class

Classes:
    LoggerFactory

"""


from decoimpact.crosscutting.logging_logger import LoggingLogger
from decoimpact.crosscutting.i_logger import ILogger


class LoggerFactory:
    """Factory for creating loggers"""

    @ staticmethod
    def create_logger() -> ILogger:
        """Creates a logger

        Returns:
            Logger: created logger
        """
        return LoggingLogger()
