from itertools import combinations
import sys
from math import comb

if len(sys.argv) != 4:
    print("Usage: python3 generate_input.py n_elements k subset_size")
    sys.exit(1)

n_elements = int(sys.argv[1])
k = int(sys.argv[2])
subset_size = int(sys.argv[3])

# Generate elements of S
S_elements = [f"a_{i}" for i in range(1, n_elements + 1)]  # a_1 to a_n_elements

# Calculate the total number of subsets
total_subsets = comb(n_elements, subset_size)
if total_subsets > 1000000:
    print(f"Too many subsets ({total_subsets}). Choose smaller n_elements or subset_size.")
    sys.exit(1)

with open('instances/input_generated.in', 'w') as file:
    file.write(f'{k}\n')  # Write k to the first line
    file.write(' '.join(S_elements) + '\n')  # Write elements of S

    # Generate all subsets of size 'subset_size' and write them to the file
    for subset in combinations(S_elements, subset_size):
        file.write(' '.join(subset) + '\n')
