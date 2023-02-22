"""
Tests for utility functions regarding an xarray dataset
"""

import pytest
import xarray as _xr

import decoimpact.business.utils.dataset_utils as utilities


def test_dataset_contains_variable_after_addition():
    """Test if new dataset contains variable after addition"""

    # Arrange
    variable = _xr.DataArray()
    variable_name = "test_variable"

    dataset = _xr.Dataset()
    # Act
    utilities.add_variable(dataset, variable, variable_name)

    # Assert
    assert dataset.__contains__(variable_name)


def test_add_incorrect_variable_to_dataset_throws_exception():
    """Test if add variable throws exception when variable to be
    added is not an XArray array"""

    # Arrange
    variable = None
    variable_name = "test_variable"

    dataset = _xr.Dataset()
    # Act
    with pytest.raises(ValueError) as error:
        utilities.add_variable(dataset, variable, variable_name)

    # Assert
    assert error.value.args[0] == "ERROR: Cannot add variable to dataset"


def test_remove_variable_remove_variable_and_keeps_others():
    """Test if remove dataset removes the desired variable, and
    keeps the other variables"""

    # Arrange
    variable1 = "variable1"
    variable2 = "variable2"
    variable3 = "variable3"
    dataset = _xr.Dataset(
        data_vars=dict(variable1=variable1, variable2=variable2, variable3=variable3)
    )
    variable_to_be_removed = variable2

    # Act
    dataset = utilities.remove_variable(dataset, variable_to_be_removed)

    # Assert
    assert dataset.__contains__(variable1)
    assert dataset.__contains__(variable3)
    assert not dataset.__contains__(variable2)


def test_remove_variable_throws_exception_if_dataset_does_not_contain_variable():
    """Test if remove variable throws exception when variable is not present
    in dataset"""

    # Arrange
    variable_name = "test_variable"

    dataset = _xr.Dataset()

    # Act
    with pytest.raises(ValueError) as error:
        utilities.remove_variable(dataset, variable_name)

    # Assert
    assert error.value.args[0] == "ERROR: Cannot remove variable from dataset"


def test_list_variables_in_dataset():
    """Test if list dataset returns a list containing all variables"""

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


def test_copy_dataset_return_xarray_dataset():
    """Test if copy dataset returns an XArray dataset"""

    # Arrange
    dataset1 = _xr.Dataset()

    # Act
    dataset2 = utilities.copy_dataset(dataset1)

    # Assert
    assert isinstance(dataset2, _xr.Dataset)


def test_rename_variable_returns_dataset_without_old_variable_and_with_new_variable():
    """Test if copy dataset returns an XArray dataset"""

    # Arrange
    variable1 = "variable1"
    variable2 = "variable2"
    variable3 = "variable3"
    new_name = "new_name"
    dataset1 = _xr.Dataset(
        data_vars=dict(var1=variable1, var2=variable2, var3=variable3)
    )
    # Act
    dataset2 = utilities.rename_variable(dataset1, "var1", new_name)

    # Assert
    assert isinstance(dataset2, _xr.Dataset)
    assert dataset2.__contains__(new_name)
    assert dataset2.__contains__("var2")
    assert not dataset2.__contains__("var1")
