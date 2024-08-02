# # This file is part of D-EcoImpact
# # Copyright (C) 2022-2024 Stichting Deltares
# # This program is free software distributed under the
# # GNU Affero General Public License version 3.0
# # A copy of the GNU Affero General Public License can be found at
# # https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
# """
# Tests for RuleBase class
# """

# from typing import List
# from unittest.mock import Mock

# import pytest
# import xarray as _xr

# from decoimpact.business.entities.rules.filter_extremes_rule import FilterExtremesRule
# from decoimpact.crosscutting.i_logger import ILogger


# def test_create_filter_extremes_rule_with_defaults():
#     """Test creating a filter extremes rule with defaults"""

#     # Arrange & Act
#     rule = FilterExtremesRule("test_rule_name", ["foo", "hello"], "peaks")

#     # Assert
#     assert isinstance(rule, FilterExtremesRule)
#     assert rule.name == "test_rule_name"
#     assert rule.description == ""
#     assert rule.input_variable_names == ["foo", "hello"]
#     assert rule.output_variable_name == "output"
#     assert rule.extreme_type == "peaks"


# def test_no_validate_error_with_correct_rule():
#     """Test a correct filter extremes rule validates without error"""

#     # Arrange
#     rule = FilterExtremesRule("test_rule_name", ["foo", "hello"], "peaks")

#     # Assert
#     assert isinstance(rule, FilterExtremesRule)


# @pytest.mark.parametrize(
#     "test_var, result_data",
#     [
#         [
#             [
#                 [1, 0],
#                 [0, 3],
#                 [-1, 0],
#                 [0, 4],
#                 [1, 0],
#                 [2, 5],
#                 [1, 0],
#                 [0, 6],
#                 [-3, 0],
#                 [-4, 7],
#                 [-2, 0],
#                 [-1, 8],
#                 [-3, 0],
#                 [-5, 9],
#             ]
#         ],
#         [
#             [-999, -999],
#             [-999, 3],
#             [-999, -999],
#             [-999, 4],
#             [-999, -999],
#             [2, 5],
#             [-999, -999],
#             [-999, 6],
#             [-999, -999],
#             [-999, 7],
#             [-999, -999],
#             [-1, 8],
#             [-999, -999],
#             [-999, 9],
#         ],
#     ],
# )
# def test_filter_extremes_rule(data_variable: List[float], result_data: List[float]):
#     """Make sure the calculation of the filter extremes is correct. Including
#     differing water and bed levels."""
#     logger = Mock(ILogger)
#     rule = FilterExtremesRule(
#         name="test", input_variable_names=["foo"], extreme_type="peaks"
#     )

#     # Create dataset
#     ds = _xr.Dataset(
#         {
#             "test_var": (["time", "mesh2d_nFaces"], data_variable),
#         }
#     )

#     value_array = ds["test_var"]

#     filter_extremes = rule.execute(value_array, logger)

#     result_array = _xr.DataArray(
#         result_data,
#         dims=["time", "mesh2d_nFaces"],
#     )

#     assert (
#         _xr.testing.assert_allclose(filter_extremes, result_array, atol=1e-08) is None
#     )
