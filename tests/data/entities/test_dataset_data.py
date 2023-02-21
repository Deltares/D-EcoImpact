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


def test_dataset_data_should_contain_system_mapping_after_creation():
    """The DatasetData should contain the system mapping needed
    for visualisation, after creation"""

    # Arrange
    data_dict = {
        "filename": "test.yaml",
        "variable_mapping": {"test": "new"},
    }

    # Act
    data = DatasetData(data_dict)

    # Assert
    assert "mesh2d" in data.mapping
    assert data.mapping["mesh2d"] == "mesh2d"
    assert "mesh2d_face_nodes" in data.mapping
    assert data.mapping["mesh2d_face_nodes"] == "mesh2d_face_nodes"
    assert "mesh2d_edge_nodes" in data.mapping
    assert data.mapping["mesh2d_edge_nodes"] == "mesh2d_edge_nodes"
    assert "mesh2d_face_x_bnd" in data.mapping
    assert data.mapping["mesh2d_face_x_bnd"] == "mesh2d_face_x_bnd"
    assert "mesh2d_face_y_bnd" in data.mapping
    assert data.mapping["mesh2d_face_y_bnd"] == "mesh2d_face_y_bnd"
    assert "mesh2d_face_nodes" in data.mapping
    assert data.mapping["mesh2d_flowelem_bl"] == "mesh2d_flowelem_bl"
