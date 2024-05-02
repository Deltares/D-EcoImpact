# This file is part of D-EcoImpact
# Copyright (C) 2022-2024 Stichting Deltares
# This program is free software distributed under the
# GNU Affero General Public License version 3.0
# A copy of the GNU Affero General Public License can be found at
# https://github.com/Deltares/D-EcoImpact/blob/main/LICENSE.md
"""
Module for ParserClassificationRule class

Classes:
    ParserClassificationRule
"""
from typing import Any, Dict
import numpy as _np

from decoimpact.business.entities.rules.string_parser_utils import (
    read_str_comparison,
    str_range_to_list,
    type_of_classification,
)
from decoimpact.crosscutting.i_logger import ILogger
from decoimpact.data.api.i_rule_data import IRuleData
from decoimpact.data.dictionary_utils import convert_table_element, get_dict_element
from decoimpact.data.entities.classification_rule_data import ClassificationRuleData
from decoimpact.data.parsers.i_parser_rule_base import IParserRuleBase
from decoimpact.data.parsers.validation_utils import validate_table_with_input


class ParserClassificationRule(IParserRuleBase):
    """Class for creating a ClassificationRuleData"""

    @property
    def rule_type_name(self) -> str:
        """Type name for the rule"""
        return "classification_rule"

    def parse_dict(self, dictionary: Dict[str, Any], logger: ILogger) -> IRuleData:
        """Parses the provided dictionary to a IRuleData
        Args:
            dictionary (Dict[str, Any]): Dictionary holding the values
                                         for making the rule
        Returns:
            RuleBase: Rule based on the provided data
        """
        name = get_dict_element("name", dictionary)
        input_variable_names = get_dict_element("input_variables", dictionary)
        criteria_table_list = get_dict_element("criteria_table", dictionary)
        criteria_table = convert_table_element(criteria_table_list)

        validate_table_with_input(criteria_table, input_variable_names)
        self._validate_criteria_on_overlap_and_gaps(criteria_table, logger)

        output_variable_name = get_dict_element("output_variable", dictionary)
        description = get_dict_element("description", dictionary)

        return ClassificationRuleData(
            name,
            input_variable_names,
            criteria_table,
            output_variable_name,
            description,
        )

    def _validate_criteria_on_overlap_and_gaps(self, criteria_table, logger: ILogger):
        for name, criteria in criteria_table.items():
            if name == "output":
                continue

            overlap_msg = []
            gap_msg = []

            # all_criteria = [type_of_classification(val) for val in criteria]
            # if not "larger" in all_criteria:
            #     logger.log_warning(
            #         f"""For the variable {name} no 'greater and equal to' (>=) classification is defined. All values above *** will not be classified"""
            #     )

            # if not "smaller" in all_criteria:
            #     logger.log_warning(
            #         f"""For the variable {name} no 'smaller than' (<)  classification is defined. All values below *** will not be classified"""
            #     )

            covered_values = [-_np.inf, _np.inf]

            for val in (
                val for val in criteria if (type_of_classification(val) == "larger")
            ):
                comparison_val = read_str_comparison(val, ">=")
                if covered_values[-1] > comparison_val:
                    covered_values[-1] = comparison_val

            for val in (
                val for val in criteria if (type_of_classification(val) == "smaller")
            ):
                comparison_val = read_str_comparison(val, "<")
                if covered_values[0] < comparison_val:
                    covered_values[0] = comparison_val

            if covered_values[0] > covered_values[-1]:
                overlap_msg.append(
                    f"Overlap for variable {name} in range {covered_values[-1]}:{covered_values[0]}"
                )
                covered_values = []

            if covered_values[0] == covered_values[-1]:
                covered_values = []

            if len(covered_values) == 0:
                for comparison_string in ["number", "range"]:
                    for val in (
                        val
                        for val in criteria
                        if (type_of_classification(val) == comparison_string)
                    ):
                        overlap_msg.append(
                            f"Overlap for variable {name} in  {comparison_string}: {val}"
                        )

            else:
                for val in (
                    val for val in criteria if (type_of_classification(val) == "range")
                ):
                    covered_values = []

            print("\n".join(overlap_msg))

            # covered_values = [-_np.inf, _np.inf]
            # criteria_class = type_of_classification(criteria)
            # if criteria_class == "larger":
            #     comparison_val = read_str_comparison(criteria, ">")
            #     covered_values[0] = comparison_val

            # elif criteria_class == "smaller":
            #     comparison_val = read_str_comparison(criteria, "<")
            #     covered_values[-1] = comparison_val

            # elif criteria_class == "number":
            #     covered_range = [float(val)]

            # elif criteria_class == "range":
            #     begin, end = str_range_to_list(criteria)
            #     comparison = (data >= begin) & (data <= end)
