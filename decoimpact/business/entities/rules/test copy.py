import numpy as np


def count_groups_with_value(data, value):
    # Split the array at indices where consecutive values change
    split_indices = np.where(data[:-1] != data[1:])[0] + 1
    groups = np.split(data, split_indices)
    
    # Count the number of groups with occurrences of the value
    group_count = sum(np.any(group == value) for group in groups)
    return group_count

# Example usage
data_array = np.array([0, 1, 0, 1, 1, 0, 1, 1, 1, 0])
value_to_count = 1
group_count = count_groups_with_value(data_array, value_to_count)
print(group_count)  # Output: 3
