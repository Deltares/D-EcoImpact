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
from tomlkit import value
import xarray as _xr

from decoimpact.business.entities.rules.depth_average_rule import DepthAverageRule
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
        "test_rule_name",
        ["foo", "hello"],
    )

    # Act
    valid = rule.validate(logger)

    # Assert
    assert isinstance(rule, DepthAverageRule)
    assert valid


# depths	heights		nInterfaces:	5
# 0	        1		    nLayers:	    4
# -1	    2		    nFaces:         4
# -3	    3		    time:       	2
# -6	    4
# -10
#
# valuables
# 1    1    1	 1			1	 1	  1	   1
# 2    2    2    2			2	 2	  2	   2
# 3    3	3    3			3	 3	  3	   3
# 4    4    4	 4			4	 4	  4	   4
# water_level
# 0    0    -1.5 -1.5		0	-6	  5	   -5
# bed_level
# -10  -5   -10	 -5
# output
# 3	2.2	3.294117647	2.571428571			3	0	3	0


mesh2d_nFaces = 4
mesh2d_nLayers = 4
mesh2d_nInterfaces = 5
time = 2

data_variable = _np.tile(_np.arange(4, 0, -1), (time, mesh2d_nFaces, 1))
mesh2d_interface_z = _np.array([-10, -6, -3, -1, 0])
mesh2d_flowelem_bl = _np.array([-10, -5, -10, -5])
mesh2d_s1 = _np.array([[0, 0, -1.5, -1.5], [0, -6, 5, -6]])


# Create dataset
ds = _xr.Dataset(
    {
        "var_3d": (["time", "mesh2d_nFaces", "mesh2d_nLayers"], data_variable),
        "mesh2d_interface_z": (["mesh2d_nInterfaces"], mesh2d_interface_z),
        "mesh2d_flowelem_bl": (["mesh2d_nFaces"], mesh2d_flowelem_bl),
        "mesh2d_s1": (["time", "mesh2d_nFaces"], mesh2d_s1),
    }
)


def test_depth_average_rule():
    """Make sure the calculation of the depth average is correct. Including
    differing water and bed levels."""
    logger = Mock(ILogger)
    rule = DepthAverageRule(
        name="test",
        input_variable_names=["foo"],
    )

    value_arrays = {
        "var_3d": ds["var_3d"],
        "mesh2d_interface_z": ds["mesh2d_interface_z"],
        "mesh2d_flowelem_bl": ds["mesh2d_flowelem_bl"],
        "mesh2d_s1": ds["mesh2d_s1"],
    }

    depth_average = rule.execute(value_arrays, logger)
    result_data = _xr.DataArray(
        _np.array([[3.0, 2.2, 3.29411765, 2.57142857], [3.0, _np.nan, 3.0, _np.nan]]),
        dims=["time", "mesh2d_nFaces"],
    )

    print(result_data)
    assert _xr.testing.assert_equal(depth_average, result_data)


# def test_depth_average_rule_with_missing_dimensions():
#     """DepthAverageRule should give an error when a dataset with incorrect dimensions are
#     used"""
#     # create test set
#     logger = Mock(ILogger)
#     rule = DepthAverageRule(
#         name="test",
#         input_variable_names=["foo"],
#     )

#     test_data = [1.2, 0.4]
#     test_array = _xr.DataArray(test_data, name="test_with_error")

#     with pytest.raises(ValueError) as exc_info:
#         rule.execute(test_array, logger)

#     exception_raised = exc_info.value

#     # Assert
#     expected_message = "Incorrect dimensions found for test_with_error"
#     assert exception_raised.args[0] == expected_message