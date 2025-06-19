# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
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
from decoimpact.crosscutting.i_logger import ILogger


def test_create_depth_average_rule_with_defaults():
    """Test creating a depth average rule with defaults"""

    # Arrange & Act
    rule = DepthAverageRule("test_rule_name",
                            ["foo", "hello"],
                            )

    # Assert
    assert isinstance(rule, DepthAverageRule)
    assert rule.name == "test_rule_name"
    assert rule.description == ""
    assert rule.input_variable_names == ["foo", "hello"]
    assert rule.output_variable_name == "output"


def test_no_validate_error_with_correct_rule():
    """Test a correct depth average rule validates without error"""

    # Arrange
    rule = DepthAverageRule(
        "test_rule_name",
        ["foo", "hello"],
    )

    # Assert
    assert isinstance(rule, DepthAverageRule)


@pytest.mark.parametrize(
    "data_variable, mesh2d_flowelem_bl, mesh2d_s1, mesh2d_interface_z, result_data",
    [
        [
            _np.array([[[20, 40], [91, 92]]]),
            _np.array([-2, -2]),
            _np.array([[0, 0]]),
            _np.array([0, -1, -2]),
            _np.array([[30.0, 91.5]]),
        ],
        [
            _np.tile(_np.arange(4, 0, -1), (2, 4, 1)),
            _np.array([-10, -5, -10, -5]),
            _np.array([[0, 0, -1.5, -1.5], [0, -6, 5, -5]]),
            _np.array([-10, -6, -3, -1, 0]),
            _np.array(
                [[3.0, 2.2, 3.29411765, 2.57142857], [3.0, _np.nan, 2.33333, _np.nan]]
            ),
        ],
        # Added this next test as to match the example in documentation
        [
            _np.tile(_np.arange(4, 0, -1), (2, 6, 1)),
            _np.array([-7.8, -7.3, -5.2, -9.5, -7, -1.6]),
            _np.array(
                [[-1.4, -1.6, -3, -1.4, -1.6, -1.6], [0, -1.6, -3, 3, -1.6, -1.6]]
            ),
            _np.array([-8.5, -6.5, -5, -2, 0]),
            _np.array(
                [
                    [2.546875, 2.473684, 2.090909, 2.851852, 2.388889, _np.nan],
                    [2.269231, 2.473684, 2.090909, 2.2, 2.388889, _np.nan],
                ]
            ),
        ],
    ],
)
def test_depth_average_rule(
    data_variable: List[float],
    mesh2d_interface_z: List[float],
    mesh2d_flowelem_bl: List[float],
    mesh2d_s1: List[float],
    result_data: List[float],
):
    """Make sure the calculation of the depth average is correct. Including
    differing water and bed levels."""
    logger = Mock(ILogger)
    rule = DepthAverageRule(
        name="test",
        input_variable_names=["foo",
                              "mesh2d_flowelem_bl",
                              "mesh2d_s1",
                              "mesh2d_interface_z"],
    )

    # Create dataset
    ds = _xr.Dataset(
        {
            "var_3d": (["time", "mesh2d_nFaces", "mesh2d_nLayers"], data_variable),
            "mesh2d_flowelem_bl": (["mesh2d_nFaces"], mesh2d_flowelem_bl),
            "mesh2d_s1": (["time", "mesh2d_nFaces"], mesh2d_s1),
            "mesh2d_interface_z": (["mesh2d_nInterfaces"], mesh2d_interface_z),
        }
    )

    value_arrays = {
        "var_3d": ds["var_3d"],
        "mesh2d_flowelem_bl": ds["mesh2d_flowelem_bl"],
        "mesh2d_s1": ds["mesh2d_s1"],
        "mesh2d_interface_z": ds["mesh2d_interface_z"],
    }

    depth_average = rule.execute(value_arrays, logger)

    result_array = _xr.DataArray(
        result_data,
        dims=["time", "mesh2d_nFaces"],
    )

    assert _xr.testing.assert_allclose(depth_average, result_array, atol=1e-08) is None


def test_dimension_error():
    """If the number of interfaces > number of layers + 1. Give an error, no
    calculation is possible"""
    logger = Mock(ILogger)
    rule = DepthAverageRule(
        name="test",
        input_variable_names=["foo",
                              "mesh2d_flowelem_bl",
                              "mesh2d_s1",
                              "mesh2d_interface_z"],
    )

    # Create dataset
    ds = _xr.Dataset(
        {
            "var_3d": (
                ["time", "mesh2d_nFaces", "mesh2d_nLayers"],
                _np.array([[[20, 40], [91, 92]]]),
            ),
            "mesh2d_interface_z": (
                ["mesh2d_nInterfaces"],
                _np.array([0, -1, -2, -3, -4]),
            ),
            "mesh2d_flowelem_bl": (
                ["mesh2d_nFaces"],
                _np.array([-2, -2]),
            ),
            "mesh2d_s1": (["time", "mesh2d_nFaces"], _np.array([[0, 0]])),
        }
    )

    value_arrays = {
        "var_3d": ds["var_3d"],
        "mesh2d_flowelem_bl": ds["mesh2d_flowelem_bl"],
        "mesh2d_s1": ds["mesh2d_s1"],
        "mesh2d_interface_z": ds["mesh2d_interface_z"],
    }

    rule.execute(value_arrays, logger)
    logger.log_error.assert_called_with(
        "The number of interfaces should be number of layers + 1. Number of "
        "interfaces = 5. Number of layers = 2."
    )
