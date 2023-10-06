# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the 
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for YamlModelData class

Classes:
    YamlModelData

"""

from pathlib import Path
from typing import List

from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.api.i_rule_data import IRuleData


class YamlModelData(IModelData):
    """Implementation of the model data"""

    def __init__(
        self,
        name: str,
        version: str,
        datasets: List[IDatasetData],
        output_path: Path,
        rules: List[IRuleData],
    ):
        super()
        self._name = name
        self._version = version
        self._datasets = datasets
        self._output_path = output_path
        self._rules = rules

    @property
    def name(self) -> str:
        """Name of the model"""
        return self._name

    @property
    def version(self) -> str:
        """Version of the model"""
        return self._version

    @property
    def datasets(self) -> List[IDatasetData]:
        """Datasets of the model"""
        return self._datasets

    @property
    def output_path(self) -> Path:
        """Model path to the output file"""
        return self._output_path

    @property
    def rules(self) -> List[IRuleData]:
        """Rules of the model"""
        return self._rules
