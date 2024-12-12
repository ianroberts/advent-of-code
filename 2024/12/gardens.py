from aoc_common.grid import Cell, Direction


def load_data():
    with open("input", "r") as f:
        lines = ["." + l.strip() + "." for l in f]
        lines.insert(0, "." * len(lines[0]))
        lines.append("." * len(lines[0]))

    return lines


CORNER_DIRECTIONS = (
    (Direction.NORTH, Direction.NE, Direction.EAST),
    (Direction.EAST, Direction.SE, Direction.SOUTH),
    (Direction.SOUTH, Direction.SW, Direction.WEST),
    (Direction.WEST, Direction.NW, Direction.NORTH),
)


def is_corner(label, straight_a, diag, straight_b):
    """
    If I am facing the corner of a cell and point 45 degrees to my left and right,
    considering the labels of the cell I'm standing on, the two I'm pointing at,
    and the one in between them (so diagonally across the corner), determine whether
    I am looking at the corner of a fence.  There are two cases:

    1. if neither of the directly adjacent cells has the same label as me, then
       there must be fences between me and each of the adjacent cells, so I'm
       looking at the 90-degree interior angle of a corner
    2. if the directly adjacent cells both have the same label as me, but the
       diagonal cell is labelled differently, then I must be looking at the
       270-degree exterior angle of a fence corner.
    """
    return (
        # interior angle
        (straight_a != label and straight_b != label)
        or
        # exterior angle
        (straight_a == label and straight_b == label and diag != label)
    )


def fences():
    grid = load_data()

    valid_rows = range(len(grid))
    valid_cols = range(len(grid[0]))
    visited = [[ch == "." for ch in row] for row in grid]

    total_cost_perimeter = 0
    total_cost_sides = 0

    while (
        start_cell := next((Cell(r, c) for r in valid_rows for c in valid_cols if not visited[r][c]), None)
    ) is not None:
        frontier = {start_cell}
        label = start_cell.of(grid)
        area = 0
        perimeter = 0
        corners = 0
        while frontier:
            cell = frontier.pop()
            cell.set(visited, True)
            area += 1
            for nbr in cell.neighbours():
                if nbr.of(grid) != label:
                    perimeter += 1
                elif not nbr.of(visited):
                    frontier.add(nbr)

            # check the four corners of this cell to see how many of them are 90 or 270 degree fence corners
            for s1, d, s2 in CORNER_DIRECTIONS:
                if is_corner(label, (cell + s1).of(grid), (cell + d).of(grid), (cell + s2).of(grid)):
                    corners += 1

        # Finished the DFS for this connected component

        # part 1 cost is area times perimeter
        cost_part1 = area * perimeter
        # part 2 cost is area times number of sides, which by definition equals the
        # number of corners
        cost_part2 = area * corners

        print(
            f"Component with label {label} starting from {start_cell}: {area=}, {perimeter=}, {corners=}, {cost_part1=}, {cost_part2=}"
        )
        total_cost_perimeter += cost_part1
        total_cost_sides += cost_part2

    print(f"Total cost of fences based on perimeter: {total_cost_perimeter}")
    print(f"Total cost baed on number of sides: {total_cost_sides}")


if __name__ == "__main__":
    fences()
