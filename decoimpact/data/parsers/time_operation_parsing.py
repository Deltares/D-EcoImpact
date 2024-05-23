# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ParserTimeAggregationRule class

Classes:
    ParserTimeAggregationRule
"""
from typing import Tuple

from decoimpact.data.api.time_operation_type import TimeOperationType


def parse_operation_values(operation_str: str) -> Tuple[TimeOperationType, float]:
    # if operation contains percentile,
    # extract percentile value as operation_parameter from operation:
    if str.startswith(operation_str, "PERCENTILE"):
        try:
            operation_parameter = float(str(operation_str)[11:-1])
        except ValueError as exc:
            message = (
                "Operation percentile is missing valid value like 'percentile(10)'"
            )
            raise ValueError(message) from exc

        # test if operation_parameter is within expected limits:
        if operation_parameter < 0 or operation_parameter > 100:
            message = "Operation percentile should be a number between 0 and 100."
            raise ValueError(message)
        return TimeOperationType.PERCENTILE, operation_parameter

    # validate operation
    match_operation = [o for o in TimeOperationType if o.name == operation_str]
    operation_value = next(iter(match_operation), None)

    if not operation_value:
        message = (
            f"Operation '{operation_str}' is not of a predefined type. Should be in:"
            + f"{[o.name for o in TimeOperationType]}."
        )
        raise ValueError(message)

    return operation_value, 0
