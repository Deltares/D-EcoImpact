"""
Module for ModelDataBuilder class
"""

from typing import Any, Iterable, List

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

    def __init__(self) -> None:
        """"""
        self._rule_parsers = rule_parsers()

    def parse_yaml_data(self, contents: dict[Any, Any]) -> IModelData:
        """_summary_
        Args:
            contents (dict[Any, Any]): _description_
        Returns:
            IModelData: _description_
        """

        datasets = list(self._parse_datasets(contents))
        rules = list(self._parse_rules(contents))

        return YamlModelData("Model 1", datasets, rules)

    def _parse_datasets(self, contents: dict[str, Any]) -> Iterable[IDatasetData]:
        datasets: List[dict[str, Any]] = get_dict_element("input-data", contents)

        for dataset in datasets:
            yield DatasetData(get_dict_element("dataset", dataset))

    def _parse_rules(self, contents: dict[str, Any]) -> Iterable[IRuleData]:
        rules: List[dict[str, Any]] = get_dict_element("rules", contents)

        for rule in rules:
            rule_type_name = list(rule.keys())[0]
            rule_dict = rule[rule_type_name]

            parser = self._get_rule_data_parser(rule_type_name)

            yield parser.parse_dict(rule_dict)

    def _get_rule_data_parser(self, rule_name: str) -> IParserRuleBase:
        for parser in rule_parsers():
            if parser.rule_type_name == rule_name:
                return parser

        raise Exception(f"No parser for {rule_name}")
