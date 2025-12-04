from typing import Iterable

from aoc_common.grid import Cell


def load_input():
    with open("input", "r") as f:
        lines = [[c for c in l.strip()] for l in f]

    return lines, range(len(lines)), range(len(lines[0]))


def accessible_cells(grid: list[list[str]], vr, vc, search_set: Iterable[Cell]) -> list[Cell]:
    accessible = []
    for c in search_set:
        if c.of(grid) == "@":
            nbr = sum(
                1 if nbr.of(grid) == "@" else 0
                for nbr in c.neighbours(valid_rows=vr, valid_cols=vc, include_diagonal=True)
            )
            if nbr < 4:
                accessible.append(c)
    return accessible


def remove_rolls(grid: list[list[str]], cells: Iterable[Cell]) -> None:
    for cell in cells:
        cell.set(grid, "x")


def main():
    grid, vr, vc = load_input()
    # Start with a scan of the whole grid
    seeds = (Cell(r, c) for r in vr for c in vc)
    total_removed = 0
    i = 0
    while True:
        i += 1
        accessible = accessible_cells(grid, vr, vc, seeds)
        if not accessible:
            # no more cells can be accessed from the current seeds - we're done
            print(f"Iteration {i} removed no more cells - finished")
            break
        total_removed += len(accessible)
        remove_rolls(grid, accessible)
        # Print the running total - iteration 1 is the part 1 answer
        print(f"Iteration {i} removed {len(accessible)} cells, {total_removed} removed in total so far")

        # Optimisation:
        # in each subsequent iteration we only need to check the cells that are
        # neighbours of the ones we removed this time around - the accessibility
        # or otherwise of cells that are _not_ neighbours of something we just
        # removed will not have been affected by this iteration; if they're
        # accessible now then they were accessible before, and would already
        # have been removed in a previous step.
        seeds = set()
        seeds.update(*(c.neighbours(vr, vc, True) for c in accessible))

    print("Final grid")
    print("\n".join("".join(row) for row in grid))
    print(f"Total removed cells: {total_removed}")


if __name__ == "__main__":
    main()
