# This file is part of D-EcoImpact
# Copyright (C) 2022-2025 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for OutputFileSettings class

Classes:
    OutputFileSettings

"""

from pathlib import Path
from typing import List, Optional


class OutputFileSettings:
    """settings class used to store information about how to write the
    output file"""

    def __init__(self, application_name: str, application_version: str) -> None:
        """Creates an instance of OutputFileSettings

        Args:
            application_version (str) : version of the application
            application_name (str) : name of the application
        """
        self._application_name: str = application_name
        self._application_version: str = application_version
        self._variables_to_save: Optional[List[str]] = None
        self.source_path: Optional[Path] = None

    @staticmethod
    def validate_format(source_path: Path, output_path: Path) -> None:
        """Require supported, matching input and output formats."""
        source_suffix = source_path.suffix.lower()
        output_suffix = output_path.suffix.lower()
        if source_suffix not in (".nc", ".cgns") or output_suffix not in (
            ".nc",
            ".cgns",
        ):
            raise NotImplementedError(
                f"Unsupported input/output format: {source_path} -> {output_path}. "
                "Currently only UGrid (NetCDF) and CGNS files are supported."
            )
        if source_suffix != output_suffix:
            raise ValueError(
                f"Input {source_path} requires a {source_suffix} output file, "
                f"not {output_path}. Format conversion is not supported."
            )

    @property
    def application_name(self) -> str:
        """name of the application"""
        return self._application_name

    @property
    def application_version(self) -> str:
        """version of the application"""
        return self._application_version

    @property
    def variables_to_save(self) -> Optional[List[str]]:
        """variables to save to the output"""
        return self._variables_to_save

    @variables_to_save.setter
    def variables_to_save(self, variables_to_save: Optional[List[str]]):
        self._variables_to_save = variables_to_save
