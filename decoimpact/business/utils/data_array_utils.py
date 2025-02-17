# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""Library for utility functions regarding an xarray data-arrays"""

import xarray as _xr

from decoimpact.crosscutting.i_logger import ILogger


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

        # check if the dimension type is a datetime type
        if (
            dim_values.dtype.name == "datetime64[ns]"
            or dim_values.dtype.name == "datetime64[s]"
        ):
            return str(dim)

    message = f"No time dimension found for {variable.name}"
    logger.log_error(message)
    raise ValueError(message)
