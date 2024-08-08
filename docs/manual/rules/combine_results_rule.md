### Combine results rule

```
FORMAT
- combine_results_rule:
      name: <name_of_rule_in_text>
      description: <description_of_rule_in_text>
      operation: <statistic_opperation_applied>
      input_variables: [<list with_input_variable_names>]
      output_variable: <one_output_variable_name>
```

The combine results rule combines the output of two or more variables to one output variable. The way this data is combined depends on the operation chosen. This could be used for adding mutual exclusive results (e.g., habitat suitability based on flow velocity and water depth) or asses difference between results (e.g., waterlevel and bathymetry to get the water depth).The rule operates one or multiple  3D variables or 2D variables, independent of the time axes, as long as these all have the same dimensions and returns a single 3D or 2D result, either with time axis, depending on input.

Operations available: Add, Subtract, Multiply, Average, Median, Min and Max

The rule needs to be applied to an existing 2D/3D variables with or without time axis. A new 2D/3D variable with or without time axis is created when the rule is executed.

```
#EXAMPLE  : Calculate bathymetry over time
# This is just an example, there is a variable bed level without time (mesh2d_flowelem_bl)

- combine_results_rule:
      name: Calculate bathymetry
      description: Calculate bathymetry over time by adding water level and water depth
      operation: subtract
      input_variables: ["water_level","water_depth"]
      output_variable: bathymetry_time

```

![Result Combine rule](../../assets/images/3_result_combine.png "Water level (in m NAP, left-hand top side) and water depth (in m NAP, right-hand top side) are combined by subtracting to create the bathymetry over time (right-hand bottom side) while maintaining the time and face dimension (layer dimension is not present in this example, but would be maintained). ")

![Result Combine rule 2](../../assets/images/3_result_combine_2.png "Water level (in m NAP, left-hand top side) and water depth (in m NAP, right-hand top side) are combined by subtracting to create the bathymetry over time (right-hand bottom side) while maintaining the time and face dimension (layer dimension is not present in this example, but would be maintained). ")

