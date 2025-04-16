# Given an integer array, return the sub-array with maximum sum, along with that maximum sum

def max_subarray(nums):
    if not nums:
        return 0, []

    max_sum = nums[0] # Initialize with first element
    current_sum = nums[0] # Track current sub array sum

    # Track the starting and ending indices of the maximum subarray
    max_start = 0
    max_end = 0
    current_start = 0

    # Star from the second element
    for i in range(1, len(nums)):
        # If current element is better than extending previous subarray
        # That is, either continue the previous subarray or start a new one
        if nums[i] > current_sum + nums[i]:
            current_sum = nums[i]
            current_start = i  # Start a new subarray
        else:
            current_sum = current_sum + nums[i]  # Extend the existing subarray

        # Update maximum if we found a better subarray
        if current_sum > max_sum:
            max_sum = current_sum
            max_start = current_start
            max_end = i

    # Extract the subarray using the tracked indices
    result_subarray = nums[max_start:max_end+1]

    return max_sum, result_subarray

# Test cases
print(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))  # Output: (6, [4, -1, 2, 1])
print(max_subarray([1]))                               # Output: (1, [1])
print(max_subarray([5, 4, -1, 7, 8]))                  # Output: (23, [5, 4, -1, 7, 8])
print(max_subarray([-1]))                              # Output: (-1, [-1])