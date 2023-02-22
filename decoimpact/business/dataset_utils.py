import xarray as _xr


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