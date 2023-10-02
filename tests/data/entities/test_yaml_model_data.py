# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares and D-EcoImpact contributors
# This program is free software distributed under the 
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for YamlModelData class
"""


from unittest.mock import Mock

import xarray as _xr

from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.entities.dataset_data import DatasetData
from decoimpact.data.entities.multiply_rule_data import MultiplyRuleData
from decoimpact.data.entities.yaml_model_data import YamlModelData


def test_yaml_model_data_default_settings_and_type():
    """Test if the YamlModelData implements the IModelData
    interface and gives the right default settings"""

    # Arrange
    datasets = [Mock(DatasetData)]
    rules = [Mock(MultiplyRuleData)]
    output_dataset = Mock(_xr.Dataset)

    # Act
    model_data = YamlModelData("Model 1", datasets, output_dataset, rules)

    # Assert

    # implements interface
    assert isinstance(model_data, IModelData)

    assert model_data.name == "Model 1"
    assert model_data.datasets == datasets
    assert isinstance(model_data.datasets[0], IDatasetData)
    assert model_data.rules == rules
    assert isinstance(model_data.rules[0], IRuleData)
