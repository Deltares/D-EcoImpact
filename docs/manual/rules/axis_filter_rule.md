### Axis filter rule

```
FORMAT
- axis_filter_rule:
      name: <name_of_rule_in_text>
      description: <description_of_rule_in_text>
      axis_name: <name_of_axis_applied>
      layer_number: <integer_nr_of_layer_in_axis_applied>
      input_variable: <one_3D_input_variable_name>
      output_variable: <one_output_variable_name> 
```

The axis filter rule is close to the layer_filter_rule, however it allows for filtering on any axis present in the data. This allows for the selection of a specific time step, spatial cell or other data axis value.

The rule needs to be applied to an existing 2D/3D variables with or without time axis. A new 2D/3D variable with or without time axis is created when the rule is executed, with the exception of the axis that was filtered upon.

```
#EXAMPLE  : Select only the salinity in the cell for the channel entrance from the faces
  - axis_filter_rule:
      name: Filter face of channel entrance (13th face cell)
      description: Filter face of channel entrance (13th face cell)
      axis_name: mesh2d_nFaces
      layer_number: 13
      input_variable: IN_salinity_PSU
      output_variable: salinity_PSU_channel_entrance
```

![Result Axis filter rule](../../assets/images/3_result_axis_filter.png "Salinity(in PSU, left-hand) is subset so that only face cell 13 is left (channel entrance) reducing the data to a 2D salinity plot for multiple time steps (in PSU, right-hand) while maintaining in this case the time dimension and layer dimension (face dimension is selected upon in this example and is therefore omitted in the results). ")
