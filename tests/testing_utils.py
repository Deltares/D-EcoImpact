"""
Helper module for test utilities
"""

from os import getenv
from logging import LogRecord
from pytest import LogCaptureFixture


def find_log_message_by_level(captured_log: LogCaptureFixture, level: str) -> LogRecord:
    """Finds the correct record from the captured_log using the provided level
    Only one message is expected to be found

    Args:
        captured_log (LogCaptureFixture): captured log messages
                                          (just add "caplog: LogCaptureFixture"
                                          to your test method)
        level (str): level of the log message (like "INFO" or "ERROR")

    Returns:
        LogRecord: found record for the provided log level

    """
    records = list(filter(lambda r: r.levelname == level, captured_log.records))

    # expect only one message for the provided level
    assert len(records) == 1

    return records[0]


def get_test_data_path() -> str:
    """Creates default test data folder path based on current test path

    Returns:
        str: path to the default test data folder
    """
    test_info: str = getenv('PYTEST_CURRENT_TEST', "")
    return test_info.split(".py::")[0] + "_data"
