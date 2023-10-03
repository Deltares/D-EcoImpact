# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the 
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for ModelDataBuilder class
"""

from typing import Any

import pytest
from mock import Mock

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.entities.model_data_builder import ModelDataBuilder

contents: dict[str, Any] = dict(
    {
        "input-data": [
            {"dataset": {"filename": "test", "variable_mapping": {"foo": "bar"}}}
        ],
        "rules": [
            {
                "multiply_rule": {
                    "name": "testrule",
                    "description": "test_mr_description",
                    "multipliers": [1, 2.0],
                    "input_variable": "testin",
                    "output_variable": "testout",
                }
            },
            {
                "step_function_rule": {
                    "name": "test_name_step_function_rule",
                    "description": "test_sfr_description",
                    "limit_response_table": [
                        ["limit", "response"],
                        [1, 10],
                        [2.0, 20],
                    ],
                    "input_variable": "test_in_sfr",
                    "output_variable": "test_out_sfr",
                }
            },
        ],
        "output-data": {"filename": "test"},
    }
)


def test_model_data_builder_parse_dict_to_model_data():
    """The ModelDataBuilder should parse the provided dictionary
    to a IModelData object"""

    # Arrange
    logger = Mock(ILogger)

    # Act
    data = ModelDataBuilder(logger)
    parsed_data = data.parse_yaml_data(contents)

    # Assert
    assert isinstance(parsed_data, IModelData)


def test_model_data_builder_gives_error_when_rule_not_defined():
    """The ModelDataBuilder should throw an exception
    when one of the rules is not defined"""

    # Arrange
    logger = Mock(ILogger)

    # Act
    data = ModelDataBuilder(logger)
    contents["rules"][0] = {"wrong_rule": "test"}

    with pytest.raises(KeyError) as exc_info:
        data.parse_yaml_data(contents)

    exception_raised = exc_info.value

    # Assert
    exc = exception_raised.args[0]
    assert exc.endswith("No parser for wrong_rule")
