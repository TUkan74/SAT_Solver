import subprocess
from argparse import ArgumentParser
from itertools import combinations

def load_instance(input_file_name):
    # Read the input instance
    with open(input_file_name, "r") as file:
        k = int(next(file))
        S_line = next(file)
        S = set(S_line.strip().split())
        C = []
        for line in file:
            if line.strip():
                subset = set(line.strip().split())
                C.append(subset)
    return S, C, k

def var_x(i):
    # Selection variable x_i for set C_i
    return i  # Variables start from 1

def encode(S, C, k):
    clauses = []
    m = len(C)
    total_vars = m  # Only selection variables x_i

    # Pairwise Distinction Constraints
    element_list = list(S)
    n_elements = len(element_list)
    for i in range(n_elements):
        for j in range(i + 1, n_elements):
            u = element_list[i]
            v = element_list[j]
            indices = [idx for idx, Ci in enumerate(C) if (u in Ci) ^ (v in Ci)]
            if not indices:
                # No set distinguishes this pair; instance is unsatisfiable
                return None, total_vars
            clause = [var_x(idx + 1) for idx in indices] + [0]
            clauses.append(clause)

    # At-Most-k Constraint
    # For small m and k, we can use the "at-most-k" encoding by prohibiting all combinations of k+1 variables
    if k < m:
        variable_indices = range(1, m + 1)
        for combination in combinations(variable_indices, k + 1):
            clause = [-var_x(i) for i in combination] + [0]
            clauses.append(clause)

    return clauses, total_vars

def call_solver(clauses, nr_vars, output_name, solver_name, verbosity):
    # Write CNF into a file in DIMACS format
    with open(output_name, "w") as file:
        file.write("p cnf " + str(nr_vars) + " " + str(len(clauses)) + '\n')
        for clause in clauses:
            file.write(' '.join(str(lit) for lit in clause) + '\n')

    # Call the solver and return the output
    return subprocess.run(['./' + solver_name, '-model', '-verb=' + str(verbosity), output_name], stdout=subprocess.PIPE)

def print_result(result, C):
    # Print the SAT solver's output
    for line in result.stdout.decode('utf-8').split('\n'):
        print(line)

    # Check if the problem is satisfiable
    if result.returncode == 20:
        print("\nInstance is UNSATISFIABLE: No such sub-collection exists.")
        return
    elif result.returncode != 10:
        print("\nError: SAT solver did not return a satisfiable or unsatisfiable result.")
        return

    # Parse the model from the solver's output
    model = []
    for line in result.stdout.decode('utf-8').split('\n'):
        if line.startswith("v"):
            vars_in_line = line.strip().split()[1:]  # Remove 'v' and split
            model.extend(int(v) for v in vars_in_line if v != '0')
    if not model:
        print("\nNo model found in solver output.")
        return

    # Extract selected sets
    selected_sets = []
    for idx, val in enumerate(model):
        var_num = abs(val)
        if var_num <= len(C) and val > 0:
            selected_sets.append((var_num, C[var_num - 1]))

    # Print the selected sets
    print("\nSelected sets (D):")
    for idx, subset in selected_sets:
        print(f"C_{idx}: " + " ".join(subset))

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        default="input.in",
        type=str,
        help=(
            "The instance file."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        default="formula.cnf",
        type=str,
        help=(
            "Output file for the DIMACS format (i.e., the CNF formula)."
        ),
    )
    parser.add_argument(
        "-s",
        "--solver",
        default="glucose-syrup_static",
        type=str,
        help=(
            "The SAT solver to be used."
        ),
    )
    parser.add_argument(
        "-v",
        "--verb",
        default=1,
        type=int,
        choices=range(0, 3),
        help=(
            "Verbosity of the SAT solver used."
        ),
    )
    args = parser.parse_args()

    # Load the input instance
    S, C, k = load_instance(args.input)

    # Encode the problem to create CNF formula
    clauses, nr_vars = encode(S, C, k)
    if clauses is None:
        print("Instance is UNSATISFIABLE: No set distinguishes some pairs.")
        exit(20)  # Return code for UNSAT

    # Call the SAT solver and get the result
    result = call_solver(clauses, nr_vars, args.output, args.solver, args.verb)

    # Interpret the result and print it in a human-readable format
    print_result(result, C)
