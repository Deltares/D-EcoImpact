"""
Tests for LoggingLogger class
"""


from decoimpact.crosscutting.logger import Logger
from decoimpact.crosscutting.logger_factory import LoggerFactory
from decoimpact.crosscutting.logging_logger import LoggingLogger


def test_create_default_logger_using_factory():
    """Test creating the default logger"""

    # Arrange & Act
    logger = LoggerFactory.create_logger()

    # Assert

    # implements base class
    assert isinstance(logger, Logger)

    # currently expected default logger
    assert isinstance(logger, LoggingLogger)
