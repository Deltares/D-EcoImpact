### Layer filter rule

```
FORMAT
- layer_filter_rule:
      name: <name_of_rule_in_text>
      description: <description_of_rule_in_text>
      layer_number: <integer_nr_of_layer>
      input_variable: <one_3D_input_variable_name>
      output_variable: <one_output_variable_name>

```

The layer filter rule allows for the extraction of a layer from 3D variables. This could be used for extracting the top layer or bottom layer (e.g., from a multi layered model result). The rule operates on all layers in a 3D variable (in the vertical) as in the time axes and returns a 2D result with the time axes intact. The rule needs to be applied to an existing 3D variable. A new 2D variable is created when the rule is executed.

```
#EXAMPLE  : Extracts the chloride concentration at surface.
  - layer_filter_rule:
      name: Extract chloride at surface
      description: Extracts the chloride concentration at surface
      layer_number: 22
      input_variable: chloride
      output_variable: chloride_top_layer

```

![Result Layer filter rule](../../assets/images/3_result_layer_filter.png "Chloride (in mg/L, left-hand side) in 3D has been filtered to a 2D result on only the 22 vertical layer (right-hand side) while maintaining the time and face dimensions.")

