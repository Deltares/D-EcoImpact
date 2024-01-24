# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""Library for utility functions regarding an xarray dataset"""

from typing import List, Optional

import xarray as _xr

from decoimpact.crosscutting.i_logger import ILogger


def add_variable(
    dataset: _xr.Dataset, variable: _xr.DataArray, variable_name: str
) -> _xr.Dataset:
    """Add variable to dataset.

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

    dataset[variable_name] = (variable.dims, variable.data)
    try:
        dataset[variable_name] = (variable.dims, variable.data)
    except ValueError as exc:
        raise ValueError("ERROR: Cannot add variable to dataset") from exc

    return dataset


def remove_variables(dataset: _xr.Dataset, variables: list[str]) -> _xr.Dataset:
    """Remove variable from dataset

    Args:
        dataset (_xr.Dataset): Dataset to remove variable from
        variables (str/list): Variable(s) to remove

    Raises:
        ValueError: When variable can not be removed

    Returns:
        _xr.Dataset: Original dataset
    """
    try:
        dataset = dataset.drop_vars(variables)
    except ValueError as exc:
        raise ValueError(f"ERROR: Cannot remove {variables} from dataset.") from exc
    return dataset


def remove_all_variables_except(dataset: _xr.Dataset, 
                                variables_to_use: List[str]) -> _xr.Dataset:
    """Remove all variables from dataset except provided list of variables.

    Args:
        dataset (_xr.Dataset): Dataset to remove variables from
        variables_to_use (List[str]): selected variables to keep

    Returns:
        _xr.Dataset: reducded dataset (containing selected variables)
    """
    all_variables = list_vars(dataset)

    variables_to_remove = [x for x in all_variables if x not in variables_to_use]

    cleaned_dataset = remove_variables(dataset, variables_to_remove)

    return cleaned_dataset


def list_vars(dataset: _xr.Dataset) -> list[str]:
    """List variables in dataset

    Args:
        dataset (_xr.Dataset): Dataset to list variables from

    Returns:
        list_variables
    """
    return list((dataset.data_vars or {}).keys())


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
        raise ValueError("ERROR: Cannot copy dataset.") from exc
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
    mapping_dict = {variable_old: variable_new}
    try:
        output_dataset = dataset.rename(mapping_dict)
    except ValueError as exc:
        raise ValueError(
            f"ERROR: Cannot rename variable {variable_old} to {variable_new}."
        ) from exc
    return output_dataset


def merge_datasets(dataset1: _xr.Dataset, dataset2: _xr.Dataset) -> _xr.Dataset:
    """Merge two datasets into one dataset.

    Args:
        dataset1 (_xr.Dataset): Dataset 1 to merge
        dataset2 (_xr.Dataset): Dataset 2 to merge

    Raises:
        ValueError: When datasets cannot be merged

    Returns:
        _xr.Dataset: Original dataset
    """
    try:
        output_dataset = dataset1.merge(dataset2, compat="identical")
    except ValueError as exc:
        raise ValueError(f"ERROR: Cannot merge {dataset1} and {dataset2}.") from exc
    return output_dataset


def merge_list_of_datasets(list_datasets: list[_xr.Dataset]) -> _xr.Dataset:
    """Merge list of datasets into 1 dataset

    Args:
        list_datasets (list): list of datasets to merge

    Raises:
        ValueError: When datasets cannot be merged

    Returns:
        _xr.Dataset: Original dataset
    """
    try:
        output_dataset = _xr.merge(list_datasets, compat="identical")
    except ValueError as exc:
        raise ValueError(f"ERROR: Cannot merge {list_datasets}.") from exc
    return output_dataset


def get_dummy_variable_in_ugrid(dataset: _xr.Dataset) -> list:
    """Get the name of the variable that serves as the dummy variable in the UGrid.

    Args:
        dataset (_xr.Dataset): Dataset to search for dummy variable

    Returns:
        str: name of the dummy variable
    """
    dummy = [
        name
        for name in dataset.data_vars
        if ("cf_role", "mesh_topology") in dataset[name].attrs.items()
    ]

    if len(dummy) == 0:
        raise ValueError(
            """No dummy variable defined and therefore input dataset does
            not comply with UGrid convention."""
        )

    return dummy


def get_dependent_vars_by_var_name(dataset: _xr.Dataset, var_name: str) -> list[str]:
    """Get all the variables that are described in the attributes of the dummy variable,
    associated with the UGrid standard.

    Args:
        dataset (_xr.Dataset): Dataset to get dependent variables from
        var_name (str): the name of the dummy variable

    Returns:
        list[str]: list of the dependent variables to copy
    """

    vars_to_check = ["_coordinates", "_connectivity", "bounds"]

    attrs_list = []

    attrs = dataset[var_name].attrs
    for attr in attrs.items():
        if any(attr[0].endswith(var_check) for var_check in vars_to_check):
            attrs_list = list(set(attrs_list + attr[1].split(" ")))
    return attrs_list


def create_composed_dataset(
    input_datasets: List[_xr.Dataset],
    variables_to_use: List[str],
    mapping: Optional[dict[str, str]],
) -> _xr.Dataset:
    """Creates a dataset based on the provided input datasets and
    the selected variables.

    Args:
        input_datasets (List[_xr.Dataset]): inputs to copy the data from
        variables_to_use (List[str]): selected variables to copy
        mapping (dict[str, str]): mapping for variables to rename after copying

    Returns:
        _xr.Dataset: composed dataset (with selected variables)
    """
    merged_dataset = merge_list_of_datasets(input_datasets)

    cleaned_dataset = remove_all_variables_except(merged_dataset, variables_to_use)

    if mapping is None or len(mapping) == 0:
        return cleaned_dataset

    return cleaned_dataset.rename_vars(mapping)


def rec_search_dep_vars(
    dataset: _xr.Dataset,
    var_list: List[str],
    dep_vars: List[str],
    checked_vars: List[str],
) -> list[str]:
    """Recursive function to loop over all variables defined in the
    attribute of the dummy variable to find which are dependent and
    also the variables that are then again dependent on those variables etc.

    Args:
        dataset (_xr.Dataset): the dataset to check
        var_list (List[str]): a list of dummy variable names to start the check
        dep_vars (List[str]): a list of dependent variables found
        checked_vars (List[str]): a list of variables that have already been
            checked in this function (it's a check so the function does not endlessly
            keep searching in the variables)

    Returns:
        list[str]: list of names of dependent variables
    """
    for var_name in var_list:
        if var_name not in checked_vars:
            dep_var = get_dependent_vars_by_var_name(dataset, var_name)
            checked_vars.append(var_name)
            if len(dep_var) > 0:
                dep_vars = list(set(dep_var + dep_vars))
                dep_vars = list(
                    set(
                        dep_vars
                        + rec_search_dep_vars(dataset, dep_var, dep_vars, checked_vars)
                    )
                )

    return dep_vars


def get_time_dimension_name(variable: _xr.DataArray, logger: ILogger) -> str:
    """Retrieves the dimension name

    Args:
        value_array (DataArray): values to get time dimension

    Raises:
        ValueError: If time dimension could not be found

    Returns:
        str: time dimension name
    """

    for dim in variable.dims:
        dim_values = variable[dim]
        if dim_values.dtype.name == "datetime64[ns]":
            return str(dim)

    message = f"No time dimension found for {variable.name}"
    logger.log_error(message)
    raise ValueError(message)
