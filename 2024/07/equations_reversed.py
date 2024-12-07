# Alternative approach that operates in reverse, starting with the desired total
# and working from right to left through the number list, repeatedly dividing,
# subtracting, or stripping off suffixes.  Working this way allows us to prune
# the search space much more radically than is possible when working from left
# to right:
#
# - for addition, prune any candidate where subtracting from the previous total
#   would go negative
# - for multiplication, prune any candidate that does not evenly divide by the
#   next number, since everything in the challenge is based on integer arithmetic
# - for digit concatenation, prune any candidate that is not a suffix of the
#   previous total
#
# The "forwards" approach took ~1.8 seconds to run for part 2, this "reverse"
# approach runs in less than 0.014 seconds (two orders of magnitude faster!).

import time
from collections import namedtuple
from typing import Callable

Problem: type[tuple[int, int, list[int]]] = namedtuple("Problem", ["total", "initial", "numbers"])


def load_data() -> list[Problem]:
    with open("input", "r") as f:
        problems = []
        for line in f:
            result, colon, args = line.strip().partition(": ")
            split_args = [int(n.strip()) for n in args.split()]
            problems.append(Problem(int(result), split_args.pop(0), list(reversed(split_args))))

    return problems


def op_add(cur_total: int, number: int) -> tuple[bool, int]:
    return number <= cur_total, cur_total - number


def op_mult(cur_total: int, number: int) -> tuple[bool, int]:
    quotient, remainder = divmod(cur_total, number)
    return remainder == 0, quotient


def op_concat(cur_total: int, number: int) -> tuple[bool, int]:
    while number > 0:
        cur_total, tot_remainder = divmod(cur_total, 10)
        number, num_remainder = divmod(number, 10)
        if num_remainder != tot_remainder:
            # we found a different digit in the result vs the operand
            return False, 0

    return True, cur_total


def solvable(*operators: Callable[[int, int], tuple[bool, int]]):
    problems = load_data()
    total_calibration = 0

    for problem in problems:
        # candidate totals from the last iteration (initially just the final total,
        # since there's been no operations yet)
        candidates = [problem.total]
        for n in problem.numbers:
            # for each number, build a new candidates list by applying all the
            # available operators to every candidate from the previous iteration,
            # but prune any answers that exceed the final expected result (since
            # all the operators we're using have the property that op(a, b) is
            # guaranteed to be greater than both a and b)
            new_candidates = []
            for c in candidates:
                for op in operators:
                    valid, val = op(c, n)
                    if valid and val >= problem.initial:
                        new_candidates.append(val)
            candidates = new_candidates
            if not candidates:
                # this equation is not satisfiable
                break  # skips the else below
        else:
            # if we get here then there was at least one candidate answer
            # that is >= problem.result, we need to check that there's one
            # that is _exactly_ equal
            if any(c == problem.initial for c in candidates):
                total_calibration += problem.total

    print(f"Total value of satisfiable equations: {total_calibration}")


if __name__ == "__main__":
    print("Part 1")
    solvable(op_add, op_mult)
    print("Part 2")
    start = time.perf_counter()
    solvable(op_add, op_mult, op_concat)
    print(f"{time.perf_counter() - start} seconds")
