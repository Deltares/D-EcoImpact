"""
Module for ModelDataBuilder class
"""

from pathlib import Path
from sqlite3 import NotSupportedError
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
        """Parse the Yaml input file into a data object"""
        print("contents", contents)

        intput_datasets = list(self._parse_input_datasets(contents))
        output_dataset = self._parse_output_dataset(contents)
        rules = list(self._parse_rules(contents))

        return YamlModelData("Model 1", intput_datasets, output_dataset, rules)

    def _parse_input_datasets(self, contents: dict[str, Any]) -> Iterable[IDatasetData]:
        input_datasets: List[dict[str, Any]] = get_dict_element("input-data", contents)

        for input_dataset in input_datasets:
            yield DatasetData(get_dict_element("dataset", input_dataset))

    def _parse_output_dataset(self, contents: dict[str, Any]) -> Path:
        output_data: dict[str, Any] = get_dict_element("output-data", contents)

        if len(output_data) != 1:
            raise NotSupportedError("Only one output is currently supported")

        return Path(output_data["filename"])

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
