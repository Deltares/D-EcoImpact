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
