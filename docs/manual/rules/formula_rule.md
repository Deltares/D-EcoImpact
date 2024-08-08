### Formula rule

```
FORMAT
- formula_rule:
      name: <name_of_rule_in_text>
      description: <description_of_rule_in_text>
      formula: <statistic_opperation_applied>
      input_variables: [<list with_input_variable_names>]
      output_variable: <one_output_variable_name>
```

With the formula based rule multiple variables can be combined in a flexible way. Operations that are supported are the standard operators.


The rule needs to be applied to an existing 2D/3D variables with or without time axis. A new 2D/3D variable with or without time axis is created when the rule is executed.

```
#EXAMPLE  : Calculate bathymetry over time
# This is just an example, there is a variable bedlevel without time (mesh2d_flowelem_bl)

- formula_rule:
      name: Calculate bathymetry
      description: Calculate bathymetry over time by adding water level and water depth
      formula: water_level + water_depth
      input_variables: ["water_level","water_depth"]
      output_variable: bathymetry_time
```

A lot of operators are supported with the formula based rule. Given two variables "x" and "y", formulas can be implemented for the following operators:

| **Operator** | **Name** | **Example** |
|:---:|:---:|:---:|
| + | Addition | x + y |
| - | Subtraction | x - y |
| * | Multiplication | x * y |
| / | Division | x / y |
| % | Modulus | x % y |
| ** | Exponentiation | x ** y |
| // | Floor division | x // y |

When a formula results in a boolean, it will be converted to a float result. Meaning that True = 1 and False = 0. Comparison, logical, identity, identity and bitwise operators are supported:

| **Operator** | **Name** | **Example** |
|:---:|:---:|:---:|
| == | Equal | x == y |
| != | Not equal | x != y |
| > | Greater than | x > y |
| < | Less than | x < y |
| >= | Greater than or equal to | x >= y |
| <= | Less than or equal to | x <= y |
| // | Floor division | x // y |
| and  | Returns True if both statements are true | x < 5 and  x < 10 |
| or | Returns True if one of the statements is true | x < 5 or x < 4 |
| not | Reverse the result, returns False if the result is true | not(x < 5 a |
| is  | Returns True if both variables are the same object | x is y |
| is not | Returns True if both variables are not the same object | x is not y |
| in  | Returns True if a sequence with the specified value is present in the object | x in y |
| not in | Returns True if a sequence with the specified value is not present in the object | x not in |

| **Operator** | **Name** | **Description** | **Example** |
|:---:|:---:|:---:|:---:|
| &  | AND | Sets each bit to 1 if both bits are 1 | x & y |
| \| | OR | Sets each bit to 1 if one of two bits is 1 | x \| y |
| ^ | XOR | Sets each bit to 1 if only one of two bits is 1 | x ^ y |
| ~ | NOT | Inverts all the bits | ~x |
| << | Zero fill left shift | Shift left by pushing zeros in from the right and let the leftmost bits fall off | x << 2 |
| >> | Signed right shift | Shift right by pushing copies of the leftmost bit in from the left, and let the rightmost bits fall off | x >> 2 |

For more information on these operators click [here](https://www.w3schools.com/python/python_operators.asp).

