# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for LoggingLogger class

Classes:
    LoggingLogger

"""

import logging as _log
from decoimpact.crosscutting.i_logger import ILogger


class LoggingLogger(ILogger):
    """Logger implementation based on default logging library"""

    def __init__(self) -> None:
        super().__init__()
        self._log = self._setup_logging()

    def log_error(self, message: str) -> None:
        """Logs an error message

        Args:
            message (str): message to log
        """
        self._log.error(message)

    def log_warning(self, message: str) -> None:
        """Logs a warning message

        Args:
            message (str): message to log
        """
        self._log.warning(message)

    def log_info(self, message: str) -> None:
        """Logs a info message

        Args:
            message (str): message to log
        """
        self._log.info(message)

    def log_debug(self, message: str) -> None:
        """Logs a debug message

        Args:
            message (str): message to log
        """
        self._log.debug(message)

    def _setup_logging(self) -> _log.Logger:
        """Sets logging information and logger setup"""
        _log.basicConfig(
            level=_log.INFO,
            format="%(asctime)s: %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M:%S",
            filename="decoimpact.log",
            encoding="utf-8",  # Only for Python > 3.9
            filemode="w",
        )

        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = _log.StreamHandler()
        console.setLevel(_log.INFO)

        # set a format which is simpler for console use
        formatter = _log.Formatter("%(asctime)s: %(levelname)-8s %(message)s")

        # tell the handler to use this format
        console.setFormatter(formatter)
        logger = _log.getLogger()

        # add the handler to the root logger
        logger.addHandler(console)

        return _log.getLogger()
