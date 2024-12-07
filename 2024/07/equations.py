import math
import operator
import time
from collections import namedtuple
from typing import Callable

Problem: type[tuple[int, list[int]]] = namedtuple("Problem", ["result", "numbers"])


def load_data() -> list[Problem]:
    with open("input", "r") as f:
        problems = []
        for line in f:
            result, colon, args = line.strip().partition(": ")
            problems.append(Problem(int(result), [int(n.strip()) for n in args.split()]))

    return problems


def solvable(*operators: Callable[[int, int], int]):
    problems = load_data()
    total_calibration = 0

    for problem in problems:
        # candidate totals from the last iteration (initially just the first number
        # itself, since there's been no operations yet)
        candidates = [problem.numbers[0]]
        for n in problem.numbers[1:]:
            # for each number, build a new candidates list by applying all the
            # available operators to every candidate from the previous iteration,
            # but prune any answers that exceed the final expected result (since
            # all the operators we're using have the property that op(a, b) is
            # guaranteed to be greater than both a and b)
            new_candidates = []
            for c in candidates:
                for op in operators:
                    val = op(c, n)
                    if val <= problem.result:
                        new_candidates.append(val)
            candidates = new_candidates
            if not candidates:
                # this equation is not satisfiable
                break  # skips the else below
        else:
            # if we get here then there was at least one candidate answer
            # that is <= problem.result, we need to check that there's one
            # that is _exactly_ equal
            if any(c == problem.result for c in candidates):
                total_calibration += problem.result

    print(f"Total value of satisfiable equations: {total_calibration}")


# The brute-force implementation of cat_digits, just turning both numbers
# to strings and back again - I originally tried something clever with
# logarithms, but that gave the wrong answer, presumably due to some sort
# of floating point over/underflow on the very large numbers.
def cat_digits(a: int, b: int) -> int:
    return int(f"{a}{b}")


# I've realised what the bug was with my original log-based impl, but this
# way is actually slower than the string-and-back-again version
def cat_digits_with_log(a: int, b: int) -> int:
    return a * (10 ** (math.floor(math.log10(b)) + 1)) + b


if __name__ == "__main__":
    print("Part 1")
    solvable(operator.add, operator.mul)
    print("Part 2")
    start = time.perf_counter()
    solvable(operator.add, operator.mul, cat_digits)
    print(f"{time.perf_counter() - start} seconds")
