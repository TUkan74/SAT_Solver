from itertools import combinations

# Generate elements of S
S_elements = [f"a_{i}" for i in range(1, 6)]  # a_1 to a_5

with open('input_small.in', 'w') as file:
    file.write('4\n')  # k = 4
    file.write(' '.join(S_elements) + '\n')
    # Generate all subsets of size 2
    for subset in combinations(S_elements, 2):
        file.write(' '.join(subset) + '\n')
