"""
Module for DatasetData interface

Classes:
    DatasetData

"""

from pathlib import Path
from typing import Any

from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.dictionary_utils import get_dict_element


class DatasetData(IDatasetData):
    """Class for storing dataset information"""

    def __init__(self, dataset: dict[str, Any]):
        """Create DatasetData based on provided info dictionary

        Args:
            dataset (dict[str, Any]):
        """
        super()
        self._path = Path(get_dict_element("filename", dataset)).resolve()
        self._combine_mappings(dataset)

    @property
    def path(self) -> Path:
        """File path to the input dataset"""
        return self._path

    @property
    def mapping(self) -> dict[str, str]:
        """Variable name mapping (source to target)"""
        return self._mapping

    def _combine_mappings(self, dataset: dict[str, Any]) -> dict[str, Any]:
        """Combines mapping specified in input file with system mapping.
        Variables in system mapping have to be included in results to enable
        XUgrid support and prevent invalid topologies.
        This also allows QuickPlot to visualize the results.

        Args:
            dataset (dict[str, Any]):
        """
        user_mapping = get_dict_element("variable_mapping", dataset, False)
        system_mapping = {
            "mesh2d": "mesh2d",
            "mesh2d_face_nodes": "mesh2d_face_nodes",
            "mesh2d_edge_nodes": "mesh2d_edge_nodes",
            "mesh2d_face_x_bnd": "mesh2d_face_x_bnd",
            "mesh2d_face_y_bnd": "mesh2d_face_y_bnd",
            "mesh2d_flowelem_bl": "mesh2d_flowelem_bl",
        }
        self._mapping = user_mapping | system_mapping
        return self._mapping
