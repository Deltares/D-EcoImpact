# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for LoggingLogger class
"""

import pytest
from pytest import LogCaptureFixture
from decoimpact.crosscutting.logging_logger import LoggingLogger
from tests.testing_utils import find_log_message_by_level


@pytest.mark.parametrize("method_name, level", [
    ("log_debug", "DEBUG"),
    ("log_info", "INFO"),
    ("log_warning", "WARNING"),
    ("log_error", "ERROR"),
])
def test_log_message_is_passed_on_to_logger(
        method_name: str,
        level: str,
        caplog: LogCaptureFixture
        ):
    """Test format of messages logged by LoggingLogger"""

    # Arrange
    logger = LoggingLogger()
    message = "test message"

    # Act
    log_method = getattr(logger, method_name)
    log_method(message)

    # Assert
    record = find_log_message_by_level(caplog, level)
    assert record.message == message
