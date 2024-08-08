### Time aggregation rule

```
FORMAT
- time_aggregation_rule:
      name: <name_of_rule_in_text>
      description: <description_of_rule_in_text>
      operation: <statistic_opperation_applied>
      time_scale : <time_aggregation_applied>
      input_variable: <one_input_variable_name>
      output_variable: <one_output_variable_name>
```

The time aggregation rule allows for calculating a statistical summary over the time axes of 3D and 2D variables. This could be used for calculating the maximum value over a year (e.g., for water level) or the minimum value over a month (e.g., oxygen concentration). The rule operates both on 3D variables and 2D variables as long as they have a time axis and returns a 3D or 2D result depending on input with the statistic calculated for a new time axis (e.g., year or month).
Operations available: Add, Average, Median, Min, Max, period statistics, Stdev and Percentile(n). When using percentile, add a number for the nth percentile with brackets like this: percentile(10). Stdev calculates the standard- deviation over the time period. Under period statistics are explained further in the text.

Time aggregation available: Year, Month

The rule needs to be applied to an existing 2D/3D variable with time axis. A new 2D/3D variable with new time axis is created when the rule is executed. With a year timestep the result is written to the last day of the year, with a month timestep the result is written to the last day of the month per year.

```
#EXAMPLE  : Calculate the maximum water level in a year.
  - time_aggregation_rule:
      name: Maximum water level year
      description: Get maximum water level in a year
      operation: MAX
      time_scale: year
      input_variable: water_level
      output_variable: MAX_water_level_year
```

![Result Time aggregation rule](../../assets/images/3_result_time_aggregation.png "Water level (in m NAP, left-hand side) with a timestep every 10 days has been summarized to the maximum for each year (right-hand side) while maintaining the face dimension (layer dimension is not present in this example, but would be maintained).")

Period statistics: Time aggregation rule with COUNT_PERIODS, AVG_DURATION_PERIODS, MIN_DURATION_PERIODS and MAX_DURATION_PERIODS

When the operation type period statistics is used, the user needs to make sure that the input data is always consisting of only 1 and 0. If there is no such layer, the user can make a combination of for example the classification rule together with the time aggregation rule. For example, water depth can be used to check whether the cells are dry or not (this can be done with a classification rule) and with the COUNT_PERIODS operation type in the time aggregation rule the number of consecutive periods within a year or month can be calculated (nr). AVG_DURATION_PERIODS, MIN_DURATION_PERIODS and MAX_DURATION_PERIODS take the respective statistic of the duration for those consecutive periods (duration).



```
#EXAMPLE:

Calculate the number of consecutive periods of dry time monthly
    - classification_rule:
        name: Classify dry time
        description: Classify to 0 and 1 the dry time
        criteria_table:
            - ["output", "water_depth"]
            - [0, ">0.10"]
            - [1, "<0.10"]
        input_variables: ["water_depth"]
        output_variable: dry_time_classified

    - time_aggregation_rule:
        name: Count periods
        description: Count periods
        operation: COUNT_PERIODS
        time_scale: month
        input_variable: dry_time_classified
        output_variable: COUNT_PERIODS_water_level_month
```

