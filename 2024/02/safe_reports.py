from itertools import pairwise, compress
from typing import Iterable


def load_reports() -> list[list[int]]:
    with open("input", "r") as f:
        return [[int(v) for v in line.split()] for line in f]


def is_safe(report: Iterable[int]) -> bool:
    # Compute the pairwise differences - we don't actually care about the
    # order or how many times each difference occurs, just the set of
    # distinct values.
    diffs = set(y - x for x, y in pairwise(report))
    if all(d > 0 for d in diffs) or all(d < 0 for d in diffs):
        # All differences have the same sign and none of them are zero
        if all(1 <= abs(d) <= 3 for d in diffs):
            # All (absolute) diffs are between 1 and 3 inclusive
            return True

    return False


def count_safe_simple():
    reports = load_reports()
    num_safe = 0

    for report in reports:
        if is_safe(report):
            num_safe += 1

    print(f"Safe reports (simple): {num_safe}")


def count_safe_damped():
    reports = load_reports()
    num_safe = 0

    for report in reports:
        indexes = range(len(report))
        # This is kind of brute force, I'm literally checking whether the original
        # report is safe, or failing that whether any of the leave-one-out
        # subsequences are safe
        if is_safe(report) or any(is_safe(compress(report, (j != i for j in indexes))) for i in indexes):
            num_safe += 1

    print(f"Safe reports (damped): {num_safe}")


if __name__ == "__main__":
    count_safe_simple()
    count_safe_damped()
