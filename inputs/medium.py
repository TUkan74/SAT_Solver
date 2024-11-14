from itertools import combinations

# Generate elements of S
S_elements = [f"a_{i}" for i in range(1, 8)]  # a_1 to a_7

with open('input_medium.in', 'w') as file:
    file.write('5\n')  # k = 5
    file.write(' '.join(S_elements) + '\n')
    # Generate all subsets of size 3
    for subset in combinations(S_elements, 3):
        file.write(' '.join(subset) + '\n')
