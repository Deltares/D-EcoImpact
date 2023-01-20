"""
Module for Logger class

Classes:
    Logger

"""

from abc import ABC, abstractmethod


class Logger(ABC):
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
