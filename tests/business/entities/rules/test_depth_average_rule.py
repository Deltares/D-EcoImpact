# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for RuleBase class
"""

from typing import List
from unittest.mock import Mock

import numpy as _np
import pytest
import xarray as _xr

from decoimpact.business.entities.rules.depth_average_rule import DepthAverageRule
from decoimpact.business.entities.rules.multi_array_operation_type import (
    MultiArrayOperationType,
)
from decoimpact.crosscutting.i_logger import ILogger


def test_create_depth_average_rule_with_defaults():
    """Test creating a depth average rule with defaults"""

    # Arrange & Act
    rule = DepthAverageRule("test_rule_name", ["foo", "hello"])

    # Assert
    assert isinstance(rule, DepthAverageRule)
    assert rule.name == "test_rule_name"
    assert rule.description == ""
    assert rule.input_variable_names == ["foo", "hello"]
    assert rule.output_variable_name == "output"


def test_no_validate_error_with_correct_rule():
    """Test a correct depth average rule validates without error"""

    # Arrange
    logger = Mock(ILogger)
    rule = DepthAverageRule(
        "test_rule_name", ["foo", "hello"],
    )

    # Act
    valid = rule.validate(logger)

    # Assert
    assert isinstance(rule, DepthAverageRule)
    assert valid
