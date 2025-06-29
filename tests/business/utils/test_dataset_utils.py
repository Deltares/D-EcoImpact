# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for utility functions regarding an xarray dataset
"""

from unittest.mock import Mock

import pytest
import xarray as _xr

import decoimpact.business.utils.dataset_utils as utilities
from decoimpact.crosscutting.i_logger import ILogger


class TestAddVariables:
    def test_dataset_contains_variable_after_addition(self):
        """Tests if new dataset contains variable after addition."""

        # Arrange
        variable = _xr.DataArray()
        variable_name = "test_variable"

        dataset = _xr.Dataset()
        # Act
        utilities.add_variable(dataset, variable, variable_name)

        # Assert
        assert variable_name in dataset

    def test_add_incorrect_variable_to_dataset_throws_exception(self):
        """Tests if add variable throws exception when variable to be
        added is not an XArray array."""

        # Arrange
        variable = None
        variable_name = "test_variable"

        dataset = _xr.Dataset()
        # Act
        with pytest.raises(ValueError) as error:
            utilities.add_variable(dataset, variable, variable_name)

        # Assert
        assert error.value.args[0] == "ERROR: Cannot add variable to dataset"


class TestRemoveVariables:
    def test_remove_variable_and_keeps_others(self):
        """Tests if remove variable from dataset removes the desired variable, and
        keeps the other variables."""

        # Arrange
        variable1 = "variable1"
        variable2 = "variable2"
        variable3 = "variable3"
        dataset = _xr.Dataset(
            data_vars=dict(
                variable1=variable1, variable2=variable2, variable3=variable3
            )
        )
        variable_to_be_removed = [variable2]

        # Act
        dataset = utilities.remove_variables(dataset, variable_to_be_removed)

        # Assert
        assert variable1 in dataset
        assert variable3 in dataset
        assert variable2 not in dataset

    def test_leave_only_one_variable(self):
        """Tests if remove all variables except 1 variable removes all variables, and
        keeps the desired variable."""

        # Arrange
        variable1 = "variable1"
        variable2 = "variable2"
        variable3 = "variable3"
        variable4 = "variable4"
        dataset = _xr.Dataset(
            data_vars=dict(
                variable1=variable1,
                variable2=variable2,
                variable3=variable3,
                variable4=variable4,
            )
        )
        dataset["variable2"].attrs = {"cf_role": "mesh_topology"}
        variable_to_keep = [variable2]

        # Act
        dataset = utilities.remove_all_variables_except(dataset, variable_to_keep)

        # Assert
        assert variable1 not in dataset
        assert variable2 in dataset
        assert variable3 not in dataset
        assert variable4 not in dataset

    def test_reduce_for_writing_throws_exception_for_non_existing_variable(self):
        """Tests if reduce dataset for writing throws error when save_only_variable is
        not present in dataset."""

        # Arrange
        variable1 = "variable1"
        variable2 = "variable2"
        variable3 = "variable3"
        variable4 = "variable4"
        dataset = _xr.Dataset(
            data_vars=dict(
                variable1=variable1,
                variable2=variable2,
                variable3=variable3,
                variable4=variable4,
            )
        )
        dataset["variable2"].attrs = {"cf_role": "mesh_topology"}
        logger = Mock(ILogger)
        variable_to_keep = ["non_existing_variable"]

        # Assert
        with pytest.raises(OSError) as error:
            utilities.reduce_dataset_for_writing(dataset, variable_to_keep, logger)

        # Assert
        assert (
            error.value.args[0]
            == "ERROR: variable non_existing_variable is not present in dataset"
        )

    def test_leave_multiple_variables(self):
        """Tests if remove all variables except multiple variable removes all
        variables, and keeps the desired variables."""

        # Arrange
        variable1 = "variable1"
        variable2 = "variable2"
        variable3 = "variable3"
        variable4 = "variable4"
        dataset = _xr.Dataset(
            data_vars=dict(
                variable1=variable1,
                variable2=variable2,
                variable3=variable3,
                variable4=variable4,
            )
        )
        dataset["variable2"].attrs = {"cf_role": "mesh_topology"}
        variables_to_keep = [variable2, variable4]

        # Act
        dataset = utilities.remove_all_variables_except(dataset, variables_to_keep)

        # Assert
        assert variable1 not in dataset
        assert variable2 in dataset
        assert variable3 not in dataset
        assert variable4 in dataset

    def test_throws_exception_if_dataset_does_not_contain_variable(
        self,
    ):
        """Tests if remove variable throws exception when variable is not present
        in dataset."""

        # Arrange
        variable_name = "test_variable"
        list_variables = [variable_name]
        dataset = _xr.Dataset()

        # Act
        with pytest.raises(ValueError) as error:
            utilities.remove_variables(dataset, list_variables)

        # Assert
        assert (
            error.value.args[0]
            == f"ERROR: Cannot remove {list_variables} from dataset."
        )


def test_list_variables_in_dataset():
    """Tests if list dataset returns a list containing all variables."""

    # Arrange
    variable1 = "variable1"
    variable2 = "variable2"
    variable3 = "variable3"
    dataset = _xr.Dataset(
        data_vars=dict(variable1=variable1, variable2=variable2, variable3=variable3)
    )

    # Act
    list_vars = utilities.list_vars(dataset)

    # Assert
    assert list_vars == [variable1, variable2, variable3]


# ----------- Testing: list_vars -----------


def test_copy_dataset_return_xarray_dataset():
    """Tests if copy dataset returns an XArray dataset."""

    # Arrange
    dataset1 = _xr.Dataset()

    # Act
    dataset2 = utilities.copy_dataset(dataset1)

    # Assert
    assert isinstance(dataset2, _xr.Dataset)


def test_rename_variable_returns_dataset_without_old_variable_and_with_new_variable():
    """Tests if copy dataset returns an XArray dataset."""

    # Arrange
    variable1 = "variable1"
    variable2 = "variable2"
    variable3 = "variable3"
    new_name = "new_name"
    dataset1 = _xr.Dataset(
        data_vars=dict(variable1=variable1, variable2=variable2, variable3=variable3)
    )
    # Act
    dataset2 = utilities.rename_variable(dataset1, "variable1", new_name)
    # Assert
    assert isinstance(dataset2, _xr.Dataset)
    assert new_name in dataset2
    assert "variable2" in dataset2
    assert "variable1" not in dataset2


class TestMergeDatasets:
    def test_merged_dataset_is_xarray_dataset_and_contains_all_variables(self):
        """Tests if merged dataset returns an XArray dataset and contains all variables."""

        # Arrange
        variable1 = "variable1"
        variable2 = "variable2"
        dataset1 = _xr.Dataset(data_vars=dict(variable1=variable1, variable2=variable2))

        variable3 = "variable3"
        variable4 = "variable4"
        dataset2 = _xr.Dataset(data_vars=dict(variable3=variable3, variable4=variable4))

        # Act
        merged_dataset = utilities.merge_datasets(dataset1, dataset2)

        # Assert
        assert isinstance(merged_dataset, _xr.Dataset)
        assert variable1 in merged_dataset
        assert variable2 in merged_dataset
        assert variable3 in merged_dataset
        assert variable4 in merged_dataset

    def test_merged_list_of_datasets_is_xarray_dataset_and_contains_all_variables(self):
        """Tests if merged dataset returns an XArray dataset and contains all variables."""

        # Arrange
        variable1 = "variable1"
        variable2 = "variable2"
        dataset1 = _xr.Dataset(data_vars=dict(variable1=variable1, variable2=variable2))

        variable3 = "variable3"
        variable4 = "variable4"
        dataset2 = _xr.Dataset(data_vars=dict(variable3=variable3, variable4=variable4))

        variable5 = "variable5"
        variable6 = "variable6"
        dataset3 = _xr.Dataset(data_vars=dict(variable5=variable5, variable6=variable6))

        list_datasets = [dataset1, dataset2, dataset3]
        # Act
        merged_dataset = utilities.merge_list_of_datasets(list_datasets)

        # Assert
        assert isinstance(merged_dataset, _xr.Dataset)
        assert variable1 in merged_dataset
        assert variable2 in merged_dataset
        assert variable3 in merged_dataset
        assert variable4 in merged_dataset
        assert variable5 in merged_dataset
        assert variable6 in merged_dataset


class TestGetDummyVariableInUgrid:
    def test_get_dummy_variable(self):
        """Test if you receive the name of the dummy variable in a ugrid dataset"""
        # Arrange
        variable1 = "variable1"
        variable2 = "variable2"
        ds = _xr.Dataset(data_vars=dict(variable1=variable1, variable2=variable2))
        ds["variable1"].attrs = {"cf_role": "mesh_topology"}

        # Act
        dummy_variable = utilities.get_dummy_variable_in_ugrid(ds)

        # Assert
        assert dummy_variable == ["variable1"]

    def test_get_dummy_variable_fails(self):
        """Test if you receive the name of the dummy variable in a ugrid dataset"""
        # Arrange
        variable1 = "variable1"
        variable2 = "variable2"
        ds = _xr.Dataset(data_vars=dict(variable1=variable1, variable2=variable2))

        # Act
        with pytest.raises(ValueError) as error:
            utilities.get_dummy_variable_in_ugrid(ds)

        # Assert
        assert (
            error.value.args[0]
            == "No dummy variable defined and therefore input dataset does "
            "not comply with UGrid convention."
        )

    def test_get_dummy_and_dependent_var_list(self):
        """Test if you receive the name of the dummy and dependent variables variable
        in a ugrid dataset"""
        # Arrange
        var_list = ["mesh2d", "var2", "var3", "var4", "var5"]
        ds = _xr.Dataset(data_vars=dict.fromkeys(var_list))
        ds["mesh2d"].attrs = {
            "cf_role": "mesh_topology",
            "test_coordinates": "var2 var3",
            "test_dimension": "var4",
            "testbounds": "var5",
        }

        # Act
        dummy_var_name = utilities.get_dummy_variable_in_ugrid(ds)
        var_list = utilities.get_dependent_var_list(ds, dummy_var_name)

        # Assert
        assert sorted(var_list) == sorted(["var2", "var5", "var3", "mesh2d"])
        assert dummy_var_name == ["mesh2d"]


class TestGetDependentVarsByVarName:
    def test_get_dummy_variable(self):
        """Test if you receive the name of the dummy variable in a ugrid dataset"""
        # Arrange
        var_list = ["var1", "var2", "var3", "var4", "var5"]
        ds = _xr.Dataset(data_vars=dict.fromkeys(var_list))
        ds["var1"].attrs = {
            "cf_role": "mesh_topology",
            "test_coordinates": "var2 var3",
            "test_dimension": "var4",
            "testbounds": "var5",
        }

        # Act
        dummy_variable = utilities.get_dummy_variable_in_ugrid(ds)

        # Assert
        assert dummy_variable == ["var1"]

    def test_get_dummy_variable_if_none(self):
        """Test if you receive nothing if there is no dependent variables in a ugrid dataset"""
        # Arrange
        var_list = ["var1", "var2", "var3", "var4", "var5"]
        ds = _xr.Dataset(data_vars=dict.fromkeys(var_list))

        # Act
        dummy_variable = utilities.get_dependent_vars_by_var_name(ds, "var1")

        # Assert
        assert sorted(dummy_variable) == sorted([])
