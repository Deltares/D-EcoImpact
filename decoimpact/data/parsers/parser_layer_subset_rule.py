"""
Module for ParserLayerFilterRule class

Classes:
    ParserLayerFilterRule
"""
from typing import Any, Dict

from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import get_dict_element
from decoimpact.data.entities.layer_subset_rule_data import LayerSubsetRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase


class ParserLayerSubsetRule(IParserRuleBase):

    """Class for creating a LayerSubsetRuleData"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "layer_subset_rule"

    def parse_dict(self, dictionary: Dict[str, Any], logger: ILogger) -> IRuleData:
        """Parses the provided dictionary to a IRuleData
        Args:
            dictionary (Dict[str, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            RuleBase: Rule based on the provided data
        """
        name = get_dict_element("name", dictionary)
        description = get_dict_element("description", dictionary)
        input_variable_name = get_dict_element("input_variable", dictionary)

        if "layer_name" in dictionary:
            layer_name = get_dict_element("layer_name", dictionary)
            if not isinstance(layer_name, str):
                message = (
                    "Layer name should be an string, "
                    f"received a {type(layer_name)}: {layer_name}"
                )
                raise ValueError(message)
        else:
            layer_name = "mesh2d_nLayers"

        start_layer_number = get_dict_element("start_layer_number", dictionary)
        if not isinstance(start_layer_number, int):
            message = (
                "Start layer number should be an integer, "
                f"received a {type(start_layer_number)}: {start_layer_number}"
            )
            raise ValueError(message)

        end_layer_number = get_dict_element("end_layer_number", dictionary)
        if not isinstance(end_layer_number, int):
            message = (
                "End layer number should be an integer, "
                f"received a {type(end_layer_number)}: {end_layer_number}"
            )
            raise ValueError(message)
        output_variable_name = get_dict_element("output_variable", dictionary)

        return LayerSubsetRuleData(
            name,
            start_layer_number,
            end_layer_number,
            input_variable_name,
            output_variable_name,
            layer_name,
            description,
        )
