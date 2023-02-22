"""Library for utility functions regarding an xarray dataset"""

import xarray as _xr


def add_variable(
    dataset: _xr.Dataset, variable: _xr.DataArray, variable_name: str
) -> _xr.Dataset:
    """Add variable to dataset

    Args:
        dataset (_xr.Dataset): Dataset to add to
        variable (_xr.DataArray): Variable containing new data
        variable_name (str): Name of new variable

    Raises:
        ValueError: When variable can not be added

    Returns:
        _xr.Dataset: original dataset
    """
    if not isinstance(variable, _xr.DataArray):
        raise ValueError("ERROR: Cannot add variable to dataset")

    try:
        dataset[variable_name] = (variable.dims, variable.data)
    except ValueError as exc:
        raise ValueError("ERROR: Cannot add variable to dataset") from exc

    return dataset


def remove_variable(dataset: _xr.Dataset, variable: str) -> _xr.Dataset:
    """Remove variable from dataset

    Args:
        dataset (_xr.Dataset): Dataset to remove variable from
        variable (str/list): Variable(s) to remove

    Raises:
        ValueError: When variable can not be removed

    Returns:
        _xr.Dataset: Original dataset
    """
    try:
        dataset = dataset.drop_vars(variable)
    except ValueError as exc:
        raise ValueError("ERROR: Cannot remove variable from dataset") from exc
    return dataset


def list_vars(dataset: _xr.Dataset) -> list:
    """List variables in dataset

    Args:
        dataset (_xr.Dataset): Dataset to list variables from

    Returns:
        list_variables
    """
    list_variables = list(dataset.data_vars)
    return list_variables


def copy_dataset(dataset: _xr.Dataset) -> _xr.Dataset:
    """Copy dataset to new dataset

    Args:
        dataset (_xr.Dataset): Dataset to remove variable from
        variable (str): Variable to remove

    Raises:
        ValueError: When variable can not be removed

    Returns:
        _xr.Dataset: Original dataset
    """
    try:
        output_dataset = dataset.copy(deep=False)
    except ValueError as exc:
        raise ValueError("ERROR: Cannot copy dataset") from exc
    return output_dataset


def rename_variable(
    dataset: _xr.Dataset, variable_old: str, variable_new: str
) -> _xr.Dataset:
    """Rename variable in dataset

    Args:
        dataset (_xr.Dataset): Dataset to remove variable from
        variable_old (str): Variable to rename, old name
        variable_new (str): Variable to rename, new name

    Raises:
        ValueError: When variable can not be renamed

    Returns:
        _xr.Dataset: Original dataset
    """
    try:
        output_dataset = dataset.rename(variable_old=variable_new)
    except ValueError as exc:
        raise ValueError(
            f"ERROR: Cannot rename variable {variable_old} to {variable_new}"
        ) from exc
    return output_dataset
