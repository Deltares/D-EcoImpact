# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for RuleBase class
"""

from typing import List
from unittest.mock import Mock

import numpy as np
import pytest
import xarray as _xr

from decoimpact.business.entities.rules.filter_extremes_rule import FilterExtremesRule
from decoimpact.crosscutting.i_logger import ILogger


def test_create_filter_extremes_rule_with_defaults():
    """Test creating a filter extremes rule with defaults"""

    # Arrange & Act
    rule = FilterExtremesRule("test_rule_name", ["input_var"], "peaks", 5, "hour", True)

    # Assert
    assert isinstance(rule, FilterExtremesRule)
    assert rule.name == "test_rule_name"
    assert rule.description == ""
    assert rule.input_variable_names == ["input_var"]
    assert rule.extreme_type == "peaks"
    assert rule.distance == 5
    assert rule.settings.time_scale == "hour"
    assert rule.mask


def test_validation_when_not_valid():
    """
    Test an incorrect filter extremes rule validates with error
    time_scale is not in TimeOperationSettings
    """
    logger = Mock(ILogger)
    rule = FilterExtremesRule("test_rule_name", ["input_var"], "peaks", 5, "h", True)

    valid = rule.validate(logger)
    assert valid is False


def test_validation_when_valid():
    """
    Test a correct filter extremes rule validates without error
    time_scale is in TimeOperationSettings
    """
    logger = Mock(ILogger)
    rule = FilterExtremesRule("test_rule_name", ["input_var"], "peaks", 5, "hour", True)

    valid = rule.validate(logger)
    assert valid


@pytest.mark.parametrize(
    "data_variable, result_data, time_data, mask, distance, time_scale, extreme_type",
    [
        # Test 1: check for multiple dimensions!
        (
            [
                [
                    [1, 0],
                    [0, 3],
                    [-1, 0],
                    [0, 4],
                    [1, 0],
                    [2, 5],
                    [1, 0],
                    [0, 6],
                    [-3, 0],
                    [-4, 7],
                    [-2, 0],
                    [-1, 8],
                    [-3, 0],
                    [-5, 9],
                ]
            ],
            [
                [
                    [np.nan, np.nan],
                    [np.nan, 3],
                    [np.nan, np.nan],
                    [np.nan, 4],
                    [np.nan, np.nan],
                    [2, 5],
                    [np.nan, np.nan],
                    [np.nan, 6],
                    [np.nan, np.nan],
                    [np.nan, 7],
                    [np.nan, np.nan],
                    [-1, 8],
                    [np.nan, np.nan],
                    [np.nan, np.nan],
                ]
            ],
            [
                np.datetime64("2005-02-25T01:30"),
                np.datetime64("2005-02-25T02:30"),
                np.datetime64("2005-02-25T03:30"),
                np.datetime64("2005-02-25T04:30"),
                np.datetime64("2005-02-25T05:30"),
                np.datetime64("2005-02-25T06:30"),
                np.datetime64("2005-02-25T07:30"),
                np.datetime64("2005-02-25T08:30"),
                np.datetime64("2005-02-25T09:30"),
                np.datetime64("2005-02-25T10:30"),
                np.datetime64("2005-02-25T11:30"),
                np.datetime64("2005-02-25T12:30"),
                np.datetime64("2005-02-25T13:30"),
                np.datetime64("2005-02-25T14:30"),
            ],
            False,
            1,
            "hour",
            "peaks",
        ),
        # Test 2: multiple times
        (
            [
                [
                    [0, 0],
                    [5, 3],
                    [0, 5],
                    [6, 4],
                    [0, 4],
                ],
                [
                    [0, 0],
                    [5, 6],
                    [0, 5],
                    [0, 7],
                    [0, 4],
                ],
            ],
            [
                [
                    [np.nan, np.nan],
                    [5, np.nan],
                    [np.nan, 5],
                    [6, np.nan],
                    [np.nan, np.nan],
                ],
                [
                    [np.nan, np.nan],
                    [5, 6],
                    [np.nan, np.nan],
                    [np.nan, 7],
                    [np.nan, np.nan],
                ],
            ],
            [
                np.datetime64("2005-02-25T01:30"),
                np.datetime64("2005-02-25T02:30"),
                np.datetime64("2005-02-25T03:30"),
                np.datetime64("2005-02-25T04:30"),
                np.datetime64("2005-02-25T05:30"),
            ],
            False,
            1,
            "hour",
            "peaks",
        ),
        # Test 3: Maks true
        (
            [
                [
                    [0, 0],
                    [5, 3],
                    [0, 5],
                    [6, 4],
                    [0, 4],
                ]
            ],
            [
                [
                    [np.nan, np.nan],
                    [1.0, np.nan],
                    [np.nan, 1.0],
                    [1.0, np.nan],
                    [np.nan, np.nan],
                ],
            ],
            [
                np.datetime64("2005-02-25T01:30"),
                np.datetime64("2005-02-25T02:30"),
                np.datetime64("2005-02-25T03:30"),
                np.datetime64("2005-02-25T04:30"),
                np.datetime64("2005-02-25T05:30"),
            ],
            True,
            1,
            "hour",
            "peaks",
        ),
        # Test 4: Different time dimension
        (
            [
                [
                    [1, 0],
                    [0, 3],
                    [-1, 0],
                    [0, 4],
                    [1, 0],
                    [2, 5],
                    [1, 0],
                    [0, 6],
                    [-3, 0],
                    [-4, 7],
                    [-2, 0],
                    [-1, 8],
                    [-3, 0],
                    [-5, 9],
                ]
            ],
            [
                [
                    [np.nan, np.nan],
                    [np.nan, np.nan],
                    [np.nan, np.nan],
                    [np.nan, 4],
                    [np.nan, np.nan],
                    [2, np.nan],
                    [np.nan, np.nan],
                    [np.nan, 6],
                    [np.nan, np.nan],
                    [np.nan, np.nan],
                    [np.nan, np.nan],
                    [-1, 8],
                    [np.nan, np.nan],
                    [np.nan, np.nan],
                ]
            ],
            [
                np.datetime64("2005-02-25T01:30"),
                np.datetime64("2005-02-25T02:30"),
                np.datetime64("2005-02-25T03:30"),
                np.datetime64("2005-02-25T04:30"),
                np.datetime64("2005-02-25T05:30"),
                np.datetime64("2005-02-25T06:30"),
                np.datetime64("2005-02-25T07:30"),
                np.datetime64("2005-02-25T08:30"),
                np.datetime64("2005-02-25T09:30"),
                np.datetime64("2005-02-25T10:30"),
                np.datetime64("2005-02-25T11:30"),
                np.datetime64("2005-02-25T12:30"),
                np.datetime64("2005-02-25T13:30"),
                np.datetime64("2005-02-25T14:30"),
            ],
            False,
            3,
            "hour",
            "peaks",
        ),
        # Test 5: Test troughs
        (
            [
                [
                    [1, 0],
                    [0, 3],
                    [-1, 0],
                    [0, 4],
                    [1, 0],
                    [2, 5],
                    [1, 0],
                    [0, 6],
                    [-3, 0],
                    [-4, 7],
                    [-2, 0],
                    [-1, 8],
                    [-3, 0],
                    [-5, 9],
                ]
            ],
            [
                [
                    [np.nan, np.nan],
                    [np.nan, np.nan],
                    [-1, 0],
                    [np.nan, np.nan],
                    [np.nan, 0],
                    [np.nan, np.nan],
                    [np.nan, 0],
                    [np.nan, np.nan],
                    [np.nan, 0],
                    [-4, np.nan],
                    [np.nan, 0],
                    [np.nan, np.nan],
                    [np.nan, 0],
                    [np.nan, np.nan],
                ]
            ],
            [
                np.datetime64("2005-02-25T01:30"),
                np.datetime64("2005-02-25T02:30"),
                np.datetime64("2005-02-25T03:30"),
                np.datetime64("2005-02-25T04:30"),
                np.datetime64("2005-02-25T05:30"),
                np.datetime64("2005-02-25T06:30"),
                np.datetime64("2005-02-25T07:30"),
                np.datetime64("2005-02-25T08:30"),
                np.datetime64("2005-02-25T09:30"),
                np.datetime64("2005-02-25T10:30"),
                np.datetime64("2005-02-25T11:30"),
                np.datetime64("2005-02-25T12:30"),
                np.datetime64("2005-02-25T13:30"),
                np.datetime64("2005-02-25T14:30"),
            ],
            False,
            1,
            "hour",
            "troughs",
        ),
    ],
)
def test_filter_extremes_rule(
    data_variable: List[float],
    result_data: List[float],
    time_data: List[float],
    mask: bool,
    distance: int,
    time_scale: str,
    extreme_type: str,
):
    """Make sure the calculation of the filter extremes is correct. Including
    differing water and bed levels."""
    logger = Mock(ILogger)
    rule = FilterExtremesRule(
        "test", ["test_var"], extreme_type, distance, time_scale, mask
    )
    assert isinstance(rule, FilterExtremesRule)
    # Create dataset
    ds = _xr.Dataset(
        {"test_var": (["dim1", "time", "dim2"], data_variable)},
        coords={
            "time": time_data,
        },
    )

    value_array = ds["test_var"]

    filter_extremes = rule.execute(value_array, logger)

    result_array = _xr.DataArray(
        result_data,
        dims=["dim1", "time", "dim2"],
        coords={
            "time": time_data,
        },
    )

    assert (
        _xr.testing.assert_allclose(filter_extremes, result_array, atol=1e-08) is None
    )
