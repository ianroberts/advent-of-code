from collections import Counter
from itertools import pairwise, compress
from typing import Iterable


def load_reports() -> list[list[int]]:
    with open("input", "r") as f:
        return [[int(v) for v in line.split()] for line in f]


def is_safe(report: Iterable[int]) -> bool:
    differences = [y - x for x, y in pairwise(report)]
    diffcount = Counter(differences)
    if all(d > 0 for d in diffcount) or all(d < 0 for d in diffcount):
        mindiff = min(abs(d) for d in diffcount)
        maxdiff = max(abs(d) for d in diffcount)
        if mindiff >= 1 and maxdiff <= 3:
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
        if is_safe(report) or any(is_safe(compress(report, (r != i for r in indexes))) for i in indexes):
            num_safe += 1

    print(f"Safe reports (damped): {num_safe}")


if __name__ == "__main__":
    count_safe_simple()
    count_safe_damped()
