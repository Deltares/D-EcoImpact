### Step function rule

```
FORMAT
- step_function_rule::
      name: <name_of_rule_in_text>
      description: <description_of_rule_in_text>
      limit_response_table:
            - [ "limit", "response"]
            - [<limit_value>, <response_value>]
            - [<limit_value>, <response_value>]
      input_variable: <one_input_variable_name>
      output_variable: <one_output_variable_name>
```

The step function rule performs stepwise classification on the provided values of 3D and 2D variables time dependent arrays. This could be used for translating variables into classes (e.g., salinity classes based on salinity) or indicate suitable/unsuitable ranges (e.g., checking whether the water level falls between the maximum and minimum water level policy criteria). The rule operates both on 3D variables and 2D variables, independent of the time axes, and returns a binominal or classes in a 3D or 2D result, either with time axis, depending on input. 

The rule needs to be applied to an existing 2D/3D variable with or without time axis. A new 2D/3D variable with or without time axis is created when the rule is executed.


```
#EXAMPLE  : Salinity classes.
    - step_function_rule:
      name: Classify salinity
      description: Make distinction between 0.0 – 0.5 , 0.5 – 1.2, 1.2 – 1.3 and >1.3 psu
      limit_response_table:
            - [ limit, response]
            - [-999.0 , 0.0 ]
            - [   0.0 , 1.0 ]
            - [   0.5 , 2.0 ]
            - [   1.2 , 3.0 ]
            - [   1.3 , 4.0 ]
            - [ 999.0 , 4.0 ]
      input_variable: salinity
      output_variable: salinity_class

```

![Visualisation of input Step function rule](../../assets/images/3_input_step.png "Salinity (in PSU) is translated in 4 distinct classes based on the shown relationship. The classes are based on 0.0 - <0.5 (class 1) 0.5 - <1.2 (class 2), 1.2 - <1.3 (class 3) and >1.3 (class 4).")

![Result Step function rule](../../assets/images/3_result_step.png "Salinity (in PSU, left-hand side) is translated in 4 distinct classes (right-hand side) while maintaining the time, face and layer dimension. The classes are based on 0.0 - <0.5 (class 1) 0.5 - <1.2 (class 2), 1.2 - <1.3 (class 3) and >1.3 (class 4).")

```
#EXAMPLE  : Check if the water level falls within the range of -0.10 and +0.15 m NAP.
  - step_function_rule:
      name: Check water level policy
      description: Check if water level is within -0.10 (minimum) and +0.15 (maximum) m NAP
      limit_response_table:
            - [ limit, response]
            - [-999.0  , 0.0 ]
            - [  -0.10 , 1.0 ]
            - [   0.15 , 0.0 ]
            - [ 999.0  , 0.0 ]
      input_variable: water_level
      output_variable : water_level_policy
```

![Visualisation of input Step function rule 2](../../assets/images/3_input_step_2.png "Water level (in m NAP) is translated in a False (0) or True (1) category by comparing it with a boundary policy based on the shown relationship. The boundary is that the water level is not allowed to be lower than -0.10 m NAP and higher than 0.15 m NAP.")

![Result Step function rule 2](../../assets/images/3_result_step_2.png "Water level (in m NAP, left-hand side) is translated in a False (0) or True (1) category by comparing it with a boundary policy (right-hand side) while maintaining the time and face dimension (layer dimension is not present in this example, but would be maintained). The boundary is that the water level is not allowed to be lower than -0.10 m NAP and higher than 0.15 m NAP.")

