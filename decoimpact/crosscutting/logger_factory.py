"""
Module for LoggerFactory class

Classes:
    LoggerFactory

"""


from decoimpact.crosscutting.logging_logger import LoggingLogger
from decoimpact.crosscutting.logger import Logger


class LoggerFactory:
    """Factory for creating loggers"""

    @ staticmethod
    def create_logger() -> Logger:
        """Creates a logger

        Returns:
            Logger: created logger
        """
        return LoggingLogger()
