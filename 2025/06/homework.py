import operator
from functools import reduce
from itertools import zip_longest
from typing import Callable

# Mapping from operator character to the corresponding function
# and identity value for that operator
OPS = {
    "+": (operator.add, 0),
    "*": (operator.mul, 1),
}

def col_slice(col_indices, i):
    if i >= len(col_indices) - 1:
        # Final column - slice to the end
        return slice(col_indices[i], None)
    # else slice to one place before the start of the next column
    return slice(col_indices[i], col_indices[i + 1] - 1)

def load_input() -> list[tuple[tuple[Callable[[int, int], int], int], list[str]]]:
    with open("input", "r") as f:
        # only strip the trailing newline, not other leading and trailing
        # whitespace since that is significant for part 2
        lines = [l.strip("\n") for l in f]

    arglines = lines[:-1]
    opline = lines[-1]

    # the operator is always the leftmost place in its column, so we can
    # split things up based on the indices of the non-space characters in
    # the operator line
    col_indices = []
    for i in range(len(opline)):
        if opline[i] != " ":
            col_indices.append(i)

    # each column will be the slice from col_indices[i]:col_indices[i+1]-1,
    # (the -1 to skip the space between one column and the next), or to the
    # end of the line in the case of the final column.
    operators = [opline[col_slice(col_indices, i)].strip() for i in range(len(col_indices))]
    args = [[l[col_slice(col_indices, i)] for i in range(len(col_indices))] for l in arglines]

    # transpose the argument strings from rows to columns
    args = list(zip(*args))
    # and zip up each operator with its argument list
    return list(zip([OPS[op] for op in operators], args))


def main():
    problems = load_input()

    # part 1 - read the numbers from left to right, top to bottom
    total = 0
    for (op, unit), args in problems:
        total += reduce(op, (int(a) for a in args), unit)

    print(f"Human numbers {total=}")

    # part 2 - read the numbers down the columns - the problem statement says
    # we're supposed to read the columns from right to left but + and * are
    # commutative and associative so working LTR gives the same answer
    total = 0
    for (op, unit), args in problems:
        # transpose the row-based strings into column-based ones - I'm using
        # zip_longest because when I copied the sample data my IDE stripped
        # the trailing spaces on each line and I missed some digits in the
        # rightmost problem column.  Using zip_longest pads the shorter
        # numbers with spaces to match the longest one.
        transposed_args = ["".join(chars) for chars in zip_longest(*args, fillvalue=" ")]
        total += reduce(op, (int(a) for a in transposed_args), unit)

    print(f"Cephalopod numbers {total=}")


if __name__ == "__main__":
    main()