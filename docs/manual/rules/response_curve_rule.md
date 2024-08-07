### Response curve rule

```
FORMAT
- response_curve_rule:
      name: <name_of_rule_in_text>
      description: <description_of_rule_in_text>
      response_table:
            - [ "input", "output"]
            - [<limit_value>, <response_value>]
            - [<limit_value>, <response_value>]
      input_variable: <one_input_variable_name>
      output_variable: <one_output_variable_name>
```

The response curve rule performs a linear interpolation over the provided values of the variables of 3D and 2D variables time dependent arrays. This could be used for a fuzzy logic translation of variables into ecological responses to these variables (e.g., suitability for aquatic plants based on light availability). The rule operates both on 3D variables and 2D variables, independent of the time axes, and returns decimal or fractional values in a 3D or 2D result, either with time axis, depending on input.

The rule needs to be applied to an existing 2D/3D variable with or without time axis. A new 2D/3D variable with or without time axis is created when the rule is executed.


```
#EXAMPLE  : Response of the habitat suitability of Long-leaf pond weed
# (Potamogeton nodosus)  to water depth.
# Suitable between 0.0 – 2.0 m and highly suitable between 0.5 – 1.0 m
- response_curve_rule:
      name: HSI Pond weed water depth
      description: Reponse of Pond weed (Potamogeton nodosus) to water depth
      response_table:
           - ["input",   "output"]
           - [-999.0 ,   0.0 ]
           - [   0.0 ,   0.0 ]
           - [   0.5 ,   1.0 ]
           - [   1.0 ,   1.0 ]
           - [   2.0 ,   0.0 ]
           - [ 999.0 ,   0.0 ]
      input_variable: water_depth
      output_variable: HSI_Pnodosus_water_depth

```

![Visualisation of input Response curve rule](../../assets/images/3_input_response.png "Water depth (in m) is translated through a linear interpolation to show the suitability for P. nodosuse based on the shown relationship. The suitability is expressed in a fraction from 0.0 (unsuitable) and 1.0 (suitable).")

![Result Response curve rule](../../assets/images/3_result_response.png "Water depth (in m, left-hand side) is translated through a linear interpolation to show the suitability for P. nodosus (right-hand side) while maintaining the time, face and layer dimension. The suitability is expressed in a fraction from 0.0 (unsuitable) and 1.0 (suitable).")

