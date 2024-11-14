# README

## Problem Description

### Minimum Test Set

**Input:**

- A finite set \( S \).
- A collection \( C = \{ C_1, C_2, \dots, C_m \} \) of subsets of set \( S \).
- A positive integer \( k \leq m \).

**Question:**

Is there a subcollection \( D = \{ D_1, D_2, \dots, D_t \} \) of sets from \( C \) such that:

- \( t \leq k \), and
- for every pair of distinct elements \( u, v \in S \), there exists a set \( D_{u,v} \in D \) that contains exactly one of the elements \( u \) and \( v \).

The goal is to find the smallest possible subcollection of sets from \( C \) that "distinguishes" all pairs of elements from \( S \).

## Description of the Chosen CNF Encoding

### Variables

- **Selection variables (\( x_i \))**: For each set \( C_i \) from \( C \), we introduce a boolean variable \( x_i \). The variable \( x_i \) is true if and only if the set \( C_i \) is selected in the subcollection \( D \).

### Constraints

1. **Distinguishing constraints for pairs of elements**:

   - For each pair of distinct elements \( u, v \in S \), there must be at least one selected set \( C_i \) that contains exactly one of the elements \( u \) or \( v \).
   - **Encoding**:
     - For each pair \( (u, v) \), we create a clause:
       \[
       \bigvee_{i \in I(u,v)} x_i
       \]
       where \( I(u,v) = \{ i \mid C_i \text{ contains exactly one of the elements } u \text{ or } v \} \).

2. **Constraint on the maximum number of selected sets (\( k \))**:

   - The total number of selected sets must not exceed \( k \):
     \[
     \sum_{i=1}^{m} x_i \leq k
     \]
   - **Encoding**:
     - For small values of \( m \) and \( k \), we use a simple encoding that forbids all combinations of \( k+1 \) variables that could be simultaneously true.
     - For each combination of \( k+1 \) variables \( x_i \), we add a clause:
       \[
       \left( \bigvee_{i \in K} \lnot x_i \right)
       \]
       where \( K \) is any \( (k+1) \)-element subset of the indices of the sets.

## User Documentation for the Script

### Running the Script

The script is run from the command line as follows:

```bash
python3 sat.py -i input.in -o formula.cnf -s glucose-syrup -v 1
```

- `-i input.in`: path to the file containing the problem instance.
- `-o formula.cnf`: name of the file to write the CNF formula in DIMACS format.
- `-s glucose-syrup`: name of the executable for the SAT solver (must be in the current directory or accessible in PATH).
- `-v 1`: verbosity level of the SAT solver (0 to 2).

### Input Format

The input file is a text file with the following structure:

- First line: integer \( k \) (maximum number of selected sets).
- Second line: elements of set \( S \), separated by spaces.
- Subsequent lines: each line represents a set \( C_i \) from the collection \( C \), with elements separated by spaces.

**Example input file (`input.in`)**:

```
2
a b c
a b
b c
a c
```

### Output

If the instance is satisfiable (SATISFIABLE), the script will output:

- The output from the SAT solver (containing information about the solution).
- The list of selected sets \( D \) with their indices and elements.

If the instance is unsatisfiable (UNSATISFIABLE), the script will output:

- Information that the instance is unsatisfiable and that no such subcollection exists.

**Example output for a satisfiable instance**:

```
s SATISFIABLE
v -1 2 3 0

Selected sets (D):
C_2: b c
C_3: a c
```

### Requirements

- **Python 3**: The script is written in Python 3.
- **SAT Solver**: For example, `glucose-syrup` in a version compatible with DIMACS CNF format and capable of outputting a model (`-model`).

## Description of Included Instances

1. **Small satisfiable instance (`input_satisfiable.in`)**

   ```
    2
    a b c
    a b
    b c
    a c
   ```
   - **Description**: Set \( S = \{a, b, c\} \), collection \( C \) contains 3 sets, \( k = 2 \).
   - **Expected output**: The script finds a subcollection of 2 sets that distinguishes all pairs.

2. **Small unsatisfiable instance (`input_unsatisfiable.in`)**

   ```
    1
    a b c
    a b
    b c
    a c
   ```
   - **Description**: Same as the previous instance, but \( k = 1 \).
   - **Expected output**: The instance is unsatisfiable because one set cannot distinguish all pairs.

3. **Larger instance running non-trivially long (`input_large.in`)**

   - **Instance generation**: Set \( S \) contains 10 elements (\( a_1, a_2, …, a_{10} \)), collection \( C \) contains all subsets of size 5. \( k = 10 \).
   - **Description**: The instance is computationally challenging due to the large number of sets and pairs.
   - **Expected output**: The script runs for at least 10 seconds, and the result may be satisfiable.

## Description of Experiments

We conducted several experiments with different instances:

- **Small instances**: The script quickly solves instances with a small number of elements and sets (up to about 5 elements in \( S \) and 10 sets in \( C \)).
- **Medium-sized instances**: For instances with \( |S| \approx 10 \) and \( |C| \approx 50 \), the runtime is on the order of seconds to minutes.
- **Large instances**: For instances with \( |S| > 15 \) and large \( |C| \) (e.g., all subsets of a certain size), the runtime can increase significantly, and the SAT solver may require a lot of time or memory.

**Notes**:

- The method used to encode the constraint on the maximum number of sets (forbidding all combinations of \( k+1 \) variables) is not scalable for large \( k \) and \( m \), as the number of clauses grows combinatorially.
- For larger instances, it would be advisable to implement a more efficient encoding of the constraint (e.g., using cardinality networks or compact counters).

**Conclusion**:

- The script is suitable for solving smaller instances of the problem.
- For larger instances, it is necessary to optimize the encoding or use specialized SAT solvers or heuristics.
