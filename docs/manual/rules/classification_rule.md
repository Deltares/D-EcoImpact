### (Multiple) Classification rule

```
FORMAT
- classification_rule:
      name: <name_of_rule_in_text>
      description: <description_of_rule_in_text>
      criteria_table:
            - [ "output"       , <input_variable_name1>, <input_variable_name2>]
            - [<response_value>,       <criteria_range>,       <criteria_range>]
            - [<response_value>,       <criteria_range>,       <criteria_range>]
      input_variables: [<list with_input_variable_names>]
      output_variable: <one_output_variable_name>
```
The classification rule allows for the classification based on the range of one or multiple input vairables. The value range can be indicated in multiple ways.
This rule can be used for indicating suitability (0 or 1) or specify categories (1,2,3 etc). The rule will start with the last given criteria range row and work upwards, hence overwriting is possible. Currently there is no check whether possible ranges have been missed or are overlapping.

The rule needs to be applied to an existing 2D/3D variables with or without time axis. A new 2D/3D variable with or without time axis is created when the rule is executed.

Criteria ranges available are:

|**Criteria range**| **Example**|**Description**|
|:---:|:---:|:---:|
| "-" | "-" | Value is not applicable to category, all is allowed |
| "criteria_value" | "5" | Value is exectly the criteria value (only applicable for integers) |
| ">criteria_value" | ">1" | Value needs to larger than criteria value |
| "<criteria_value" | "<0.5" | Value needs to be smaller than criteria value |
| ">criteria_value" | ">=1" | Value needs to larger than or equal to criteria value |
| "<criteria_value" | "<=0.5" | Value needs to be smaller than or equal to criteria value |
| "criteria_value1:criteria_value2" | "0.2:4" | Value needs to be equal or be in between criteria_value1 and criteria_value2 |

```
#EXAMPLE  : Determine the suitability for aquatic vegetation based on classification
  - classification_rule:
      name: Classification for aquatic plants
      description: Derive the classification for aquatic plants based on water depth, flow velocity and chloride levels
      criteria_table:
        - ["output", "MIN_water_depth_mNAP", "MAX_flow_velocity", "MAX_chloride"]
        - [     1  ,               "<0.10" ,                "-" ,            "-"] # too dry
        - [     2  ,                ">4.0" ,                "-" ,            "-"] # too deep
        - [     3  ,                   "-" ,                "-" ,         ">400"] # too salty
        - [     4  ,                   "-" ,             ">1.5" ,            "-"] # too fast flowing
        - [     5  ,            "0.10:4.0" ,          "0.0:1.5" ,       "0:400"] # perfect for aquatic plants
      input_variables: ["MIN_water_depth_mNAP", "MAX_flow_velocity", "MAX_chloride"]
      output_variable: aquatic_plant_classes


  - classification_rule:
      name: Suitability for aquatic plants
      description: Derive the suitability for aquatic plants based on the classification
      criteria_table:
        - ["output", "aquatic_plant_classes"]
        - [     0  ,                   "1:4"] # not suitable
        - [     1  ,                     "5"] # suitable
      input_variables: ["aquatic_plant_classes"]
      output_variable: aquatic_plant_suitability

```

![Result Classification rule](../../assets/images/3_result_classification.png "Minimum Water depth(in m NAP, left-hand top side), maximum flow velocity(in m/s, right-hand top side) and maximum chloride level (in mg/L, left-hand bottom side) are combined based on criteria ranges to create the aquatic plant classification (right-hand bottom side) while maintaining the time and face dimension (layer dimension is not present in this example, but would be maintained). ")

![Result Classification rule 2](../../assets/images/3_result_classification_2.png "The aquatic plant classification (left-hand side) are translated based on criteria ranges to an aquatic_plant suitability class (right-hand side) while maintaining the time and face dimension (layer dimension is not present in this example, but would be maintained). ")

