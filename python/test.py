import random

def generate_sorted_non_negative_list(target_sum, length):
    # Generate a list of random non-negative integers
    random_list = [random.randint(1, 100) for _ in range(length)]

    # Sort the list in descending order
    random_list.sort(reverse=True)

    # Adjust the last element to make the sum equal to the target value
    random_list[-1] += target_sum - sum(random_list)

    return random_list

# Example usage
target_sum = 57
length_of_list = 10
result_list = generate_sorted_non_negative_list(target_sum, length_of_list)

print("Target Sum:", target_sum)
print("Generated List:", result_list)
print("Sum of the List:", sum(result_list))
