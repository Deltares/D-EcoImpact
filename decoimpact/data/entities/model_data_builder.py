# This file is part of D-EcoImpact
# Copyright (C) 2022-2023 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ModelDataBuilder class
"""

from pathlib import Path
from typing import Any, Iterable, List

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_dataset import IDatasetData
from decoimpact.data.api.i_model_data import IModelData
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.entities.dataset_data import DatasetData
from decoimpact.data.entities.yaml_model_data import YamlModelData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.rule_parsers import rule_parsers


class ModelDataBuilder:
    """Builder for creating Model data objects (parsing rules and datasets
    read from the input file to Rule and DatasetData objects)"""

    def __init__(self, logger: ILogger) -> None:
        """Create ModelDataBuilder"""
        self._rule_parsers = list(rule_parsers())
        self._logger = logger

    def parse_yaml_data(self, contents: dict[Any, Any]) -> IModelData:
        """Parse the Yaml input file into a data object

        Raises:
            AttributeError: when version is not available from the input file
        """
        input_version = self._parse_input_version(contents)
        if not input_version:
            raise AttributeError(name="Version not available from input file")
        input_datasets = list(self._parse_input_datasets(contents))
        output_path = self._parse_output_dataset(contents)
        print('dud',self._parse_output_variables(contents))
        output_variables = self._parse_output_variables(contents)
        print('qq',output_variables)
        rules = list(self._parse_rules(contents))

        return YamlModelData(
            "Model 1",
            input_version,
            input_datasets,
            output_path,
            output_variables,
            rules,
        )

    def _parse_input_version(self, contents: str) -> List[int]:
        input_version = None
        try:
            # read version string
            version_string: str = get_dict_element("version", contents)

            # check existence of version_string
            if len(str(version_string)) == 0 or version_string is None:
                self._logger.log_error(
                    f"Version ('{version_string}')" + " in input yaml is missing"
                )
            else:
                # split string into 3 list items
                version_list = version_string.split(".", 2)

                # convert str[] to int[]
                input_version = list(map(int, version_list))

        except (ValueError, AttributeError, TypeError) as exception:
            self._logger.log_error(f"Invalid version in input yaml: {exception}")
            return None

        return input_version

    def _parse_input_datasets(self, contents: dict[str, Any]) -> Iterable[IDatasetData]:
        input_datasets: List[dict[str, Any]] = get_dict_element("input-data", contents)

        for input_dataset in input_datasets:
            yield DatasetData(get_dict_element("dataset", input_dataset))

    def _parse_output_dataset(self, contents: dict[str, Any]) -> Path:
        output_data: dict[str, Any] = get_dict_element("output-data", contents)

        return Path(output_data["filename"])

    def _parse_output_variables(
        self, contents: dict[str, Any]
    ) -> Iterable[IDatasetData]:
        output_data: dict[str, Any] = get_dict_element("output-data", contents)
        save_only_variables = output_data.get('save_only_variables', [])

        # Convert to list if not already one
        if not isinstance(save_only_variables, list):
            save_only_variables = [save_only_variables]

        return save_only_variables

    def _parse_rules(self, contents: dict[str, Any]) -> Iterable[IRuleData]:
        rules: List[dict[str, Any]] = get_dict_element("rules", contents)

        for rule in rules:
            rule_type_name = list(rule.keys())[0]
            rule_dict = rule[rule_type_name]

            parser = self._get_rule_data_parser(rule_type_name)

            yield parser.parse_dict(rule_dict, self._logger)

    def _get_rule_data_parser(self, rule_name: str) -> IParserRuleBase:
        for parser in rule_parsers():
            if parser.rule_type_name == rule_name:
                return parser

        raise KeyError(f"No parser for {rule_name}")
