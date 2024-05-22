# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for AxisFilterRule class
"""
import xarray as _xr
from mock import Mock

from decoimpact.business.entities.rules.axis_filter_rule import AxisFilterRule
from decoimpact.crosscutting.i_logger import ILogger


def test_create_axis_filter_rule_should_set_defaults():
    """Test creating a AxisFilterRule with defaults"""

    # Arrange & Act
    rule = AxisFilterRule("test", ["foo"], 3, "boo")

    # Assert
    assert rule.name == "test"
    assert rule.description == ""
    assert rule.input_variable_names == ["foo"]
    assert rule.output_variable_name == "output"
    assert rule.layer_number == 3
    assert rule.axis_name == "boo"
    assert isinstance(rule, AxisFilterRule)


def test_execute_value_array_axis_filtered():
    """Test execute of layer filter rule"""
    # Arrange & Act
    logger = Mock(ILogger)
    rule = AxisFilterRule("test", ["foo"], 1, "dim_1")
    data = [[1, 2], [3, 4]]
    value_array = _xr.DataArray(data, dims=("dim_1", "dim_2"))
    filtered_array = rule.execute(value_array, logger)

    result_data = [1, 2]
    result_array = _xr.DataArray(result_data, dims=("dim_2"))

    # Assert
    assert _xr.testing.assert_equal(filtered_array, result_array) is None
