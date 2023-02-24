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
        "variable_mapping": {"test": "new"},
    }

    # Act
    data = DatasetData(data_dict)

    # Assert

    assert isinstance(data, IDatasetData)
    assert str(data.path).endswith("test.yaml")
    assert "test" in data.mapping
    assert data.mapping["test"] == "new"
