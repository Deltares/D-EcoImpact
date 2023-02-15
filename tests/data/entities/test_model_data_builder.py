"""
Tests for ModelDataBuilder class
"""

import pytest

from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.entities.model_data_builder import ModelDataBuilder

contents = dict(
    {
        "input-data": [
            {"dataset": {"filename": "test", "variable_mapping": {"foo": "bar"}}}
        ],
        "rules": [
            {
                "multiply_rule": {
                    "name": "testrule",
                    "description": "testdescription",
                    "multipliers": [1, 2.0],
                    "input_variable": "testin",
                    "output_variable": "testout",
                }
            }
        ],
        "output-data": [{"filename": "test"}],
    }
)


def test_model_data_builder_parse_dict_to_model_data():
    """The ModelDataBuilder should parse the provided dictionary
    to a IModelData object"""

    # Act
    data = ModelDataBuilder()

    parsed_data = data.parse_yaml_data(contents)
    assert isinstance(parsed_data, IModelData)


def test_model_data_builder_gives_error_when_rule_not_defined():
    """The ModelDataBuilder should parse the provided dictionary
    to a IModelData object"""

    # Act
    data = ModelDataBuilder()
    contents["rules"] = [{"wrong_rule": "test"}]

    with pytest.raises(KeyError) as exc_info:
        data.parse_yaml_data(contents)

    exception_raised = exc_info.value

    # Assert
    exc = exception_raised.args[0]
    assert exc.endswith("No parser for wrong_rule")
