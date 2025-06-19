# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Tests for DatasetData class
"""

from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.entities.dataset_data import DatasetData


def test_dataset_data_creation_logic():
    """The DatasetData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Arrange
    data_dict = {
        "filename": "test.yaml",
        # start_date is left out to check it is optional
        "end_date": "31-12-2020",
        "variable_mapping": {"test": "new"},
    }

    # Act
    data = DatasetData(data_dict)

    # Assert

    assert isinstance(data, IDatasetData)
    assert str(data.path).endswith("test.yaml")
    assert "test" in data.mapping
    assert data.mapping["test"] == "new"
    assert data.start_date == "None"
    assert data.end_date == "31-12-2020"


def test_dataset_data_time_filter():
    """The DatasetData should parse the provided dictionary
    to correctly initialize itself during creation
    and test the values of start and end date
    and test whether the time filter is optional"""

    # Arrange
    data_dict = {
        "filename": "test.yaml",
        "start_date": "01-01-2019",
        # end_date is left out to check it is optional
        "variable_mapping": {"test": "new"},
    }

    # Act
    data = DatasetData(data_dict)

    # Assert
    assert isinstance(data, IDatasetData)
    assert str(data.path).endswith("test.yaml")
    assert data.start_date == "01-01-2019"
    assert data.end_date == "None"
    # the result 'None' should result in not filtering the data set on end date
