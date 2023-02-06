"""
Tests for DatasetData class
"""

import xarray as _xr

from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.entities.dataset_data import DatasetData
from tests.testing_utils import get_test_data_path


def test_dataset_data_creation_logic():
    """The DatasetData should parse the provided dictionary
    to correctly initialize itself during creation"""

    # Arrange
    data_dict = {"filename": "test.yaml", "variable_mapping": {"test": "test_new"}}

    # Act
    data = DatasetData(data_dict)

    # Assert

    assert isinstance(data, IDatasetData)
    assert data.path == "test.yaml"
    assert "test" in data.mapping
    assert data.mapping["test"] == "test_new"


def test_dataset_data_get_input_dataset_should_read_file():
    """ When calling get_input_dataset on a dataset should
    read the specified IDatasetData.path to create a
    """

    # Arrange
    path = get_test_data_path() + "/FlowFM_net.nc"
    data_dict = {"filename": path, "variable_mapping": {"test": "test_new"}}
    data = DatasetData(data_dict)

    # Act
    dataset = data.get_input_dataset()

    # Assert
    assert isinstance(dataset, _xr.Dataset)
