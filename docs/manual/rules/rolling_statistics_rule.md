### Rolling statistic rule

```
FORMAT
- rolling_statistics_rule:
      name: <name_of_rule_in_text>
      description: <description_of_rule_in_text>
      operation: <statistic_opperation_applied>
      time_scale : <time_step_unit_applied>
      period: <time_step_value_applied>
      input_variable: <one_input_variable_name>
      output_variable: <one_output_variable_name>
```

The rolling statistic rule allows for a rolling statistic based on the chosen operation and the time period over which the statistic should be repeated. The calculated statistic will be written to each last timestep that falls within the period.
Operations available: Add, Average, Median, Min, Max, count_periods, Stdev and Percentile(n). When using percentile, add a number for the nth percentile with brackets like this: percentile(10).

Time scales available: hour, day
Period can be a float or integer value.

The rule needs to be applied to an existing 2D/3D variables with time axis. A new 2D/3D variable with the same time axis is created when the rule is executed.

An explanation of how the rolling statistic rule works is shown in the table below:

|**timestep**|**1**|**2**|**3**|**4**|**5**|**6**|**7**|**8**|
|:--------:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| period1  | - | - | - | i |   |   |   |   |
| period2  |   | - | - | - | i |   |   |   |
| period3  |   |   | - | - | - | i |   |   |

In the example shown above the stripe indicates the time period covered (4 timesteps in this case) and with i the location where the result of the statistic over that period is written. Hence, the first three timesteps in this example will not contain any values. This is repeated until the time series has been covered.

```
#EXAMPLE  : Determine a rolling statistic over salinity levels
  - rolling_statistics_rule:
      name: test rolling statistic 12.5 hours
      description: test rolling statistic 12.5 hours
      operation: MAX
      time_scale: hour
      period: 12.5
      input_variable: IN_salinity_PSU
      output_variable: salinity_tl_hour_max

  - rolling_statistics_rule:
      name: test rolling statistic 7 days
      description: test rolling statistic 7 days
      operation: MAX
      time_scale: day
      period: 7
      input_variable: IN_salinity_PSU
      output_variable: salinity_tl_week_max
```

![Result Rolling statistic rule](../../assets/images/3_result_rolling_statistic.png "Salinity(in PSU, left-hand) is translated to a 12.5 hourly statistic (in PSU, right-hand) while maintaining the time and face dimension (layer dimension is not present in this example, but would be maintained). ")

![Result Rolling statistic rule 2](../../assets/images/3_result_rolling_statistic_2.png "Salinity(in PSU, left-hand) is translated to an weekly statistic (in PSU, right-hand) while maintaining the time and face dimension (layer dimension is not present in this example, but would be maintained). ")

