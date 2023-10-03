# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the 
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for LoggingLogger class
"""


from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.crosscutting.logger_factory import LoggerFactory
from decoimpact.crosscutting.logging_logger import LoggingLogger


def test_create_default_logger_using_factory():
    """Test creating the default logger"""

    # Arrange & Act
    logger = LoggerFactory.create_logger()

    # Assert

    # implements base class
    assert isinstance(logger, ILogger)

    # currently expected default logger
    assert isinstance(logger, LoggingLogger)
