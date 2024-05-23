# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
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

    def __init__(self, name: str, version: List[int]):
        super()
        self._name = name
        self._version = version
        self._datasets = []
        self._output_path = Path("")
        self._output_variables = []
        self._rules = []

    @property
    def name(self) -> str:
        """Name of the model"""
        return self._name

    @property
    def version(self) -> List[int]:
        """Version of the model"""
        return self._version

    @property
    def datasets(self) -> List[IDatasetData]:
        """Datasets of the model"""
        return self._datasets

    @datasets.setter
    def datasets(self, datasets: List[IDatasetData]):
        self._datasets = datasets

    @property
    def output_path(self) -> Path:
        """Model path to the output file"""
        return self._output_path

    @output_path.setter
    def output_path(self, output_path: Path):
        self._output_path = output_path

    @property
    def output_variables(self) -> List[str]:
        """Output variables"""
        return self._output_variables

    @output_variables.setter
    def output_variables(self, output_variables: List[str]):
        self._output_variables = output_variables

    @property
    def rules(self) -> List[IRuleData]:
        """Rules of the model"""
        return self._rules

    @rules.setter
    def rules(self, rules: List[IRuleData]):
        self._rules = rules
