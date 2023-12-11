from collections import namedtuple
from bisect import bisect
Cell = namedtuple("Cell", ["row", "col"])


def parse_input():
    # Rather than build the entire matrix, all we really care about is (a) where the galaxies are
    # and (b) which rows or columns of the original matrix are completely empty.
    with open("input", "r") as f:
        galaxies = [Cell(r, c) for r, row in enumerate(f) for c, col in enumerate(row) if col == "#"]

    max_col = max(col for row, col in galaxies)
    max_row = max(row for row, col in galaxies)

    # Determine the empty rows and columns - note that this won't include empty rows at the very
    # end or columns at the far right of the grid, but that doesn't matter as we only need to know
    # about empty space *between* galaxies, not around the edge of the whole universe
    galaxy_rows = set(r for r, c in galaxies)
    empty_rows = [i for i in range(max_row+1) if i not in galaxy_rows]

    galaxy_cols = set(c for r, c in galaxies)
    empty_cols = [i for i in range(max_col+1) if i not in galaxy_cols]

    return galaxies, empty_rows, empty_cols


def shortest_paths(empty_multiplier):
    galaxies, empty_rows, empty_cols = parse_input()

    total_distance = 0
    for i, g_a in enumerate(galaxies):
        # "pairs" ignore ordering, so we only need to consider the top triangle of the full
        # cartesian product
        for g_b in galaxies[i+1:]:
            # distance between is just Manhattan metric, extended by the empty rows & cols
            row1, row2 = sorted((g_a.row, g_b.row))
            num_empty = bisect(empty_rows, row2) - bisect(empty_rows, row1)
            total_distance += row2 - row1 + num_empty * (empty_multiplier-1)

            col1, col2 = sorted((g_a.col, g_b.col))
            num_empty = bisect(empty_cols, col2) - bisect(empty_cols, col1)
            total_distance += col2 - col1 + num_empty * (empty_multiplier-1)

    return total_distance


if __name__ == "__main__":
    print(f"Total distance between all pairs - small universe = {shortest_paths(2)}")
    print(f"Total distance between all pairs - biiiig universe = {shortest_paths(1_000_000)}")
