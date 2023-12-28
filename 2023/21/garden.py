from collections import namedtuple
Cell = namedtuple("Cell", ["row", "col"])


def parse_input():
    with open("input", "r") as f:
        matrix = [l.strip() for l in f]

    r = ["S" in line for line in matrix].index(True)
    c = matrix[r].index("S")
    return matrix, Cell(r, c)


def one_step_from(matrix, points):
    new_points = set()
    rows = len(matrix)
    cols = len(matrix[0])
    for p in points:
        if matrix[(p.row-1) % rows][p.col % cols] != "#":
            new_points.add(Cell(p.row-1, p.col))
        if matrix[p.row % rows][(p.col-1) % cols] != "#":
            new_points.add(Cell(p.row, p.col-1))
        if matrix[(p.row+1) % rows][p.col % cols] != "#":
            new_points.add(Cell(p.row+1, p.col))
        if matrix[p.row % rows][(p.col+1) % cols] != "#":
            new_points.add(Cell(p.row, p.col+1))

    return new_points


def n_steps(n):
    matrix, start = parse_input()
    points = {start}
    for i in range(n):
        points = one_step_from(matrix, points)
        print(f"{i+1}\t{len(points)}")


if __name__ == "__main__":
    n_steps(64)

# Part 2: so the way the input has been constructed, after 65 steps we can reach every . square
# within the grid for which the sum of its x and y offsets from S is an odd number <= 65, except
# those squares that are completely unreachable (i.e. that have # squares on all four sides.  This
# totals 3868 squares.  From here each multiple of 131 further steps should cover every other
# reachable square in the whole grid, some more than once if we consider the grid as wrapping
# around top-to-bottom and left-to-right to model the infinite garden.
#
# Playing with these numbers:
#
# after 65+131 steps {1: 3762, 4: 3868, 2: 7567}
# after 65+2*131 steps {4: 3762, 9: 3868, 6: 7567}
# after 65+3*131 steps {9: 3762, 16: 3868, 12: 7567}
# after 65+4*131 steps {16:3762, 25: 3868, 20: 7567}
#
# pattern appears to be that after 65 + 131n steps, there are 3762 cells of the wrapped-around grid
# visited n**2 times, 3868 cells visited (n+1)**2 times, and 7567 cells visited n(n+1) times.
#
# The target number of steps 26501365 is 65 + 131*202300, so if this pattern continues then the
# final number of reachable squares should be
#
# 202300**2 * 3762 + 202301**2 * 3868 + 202300*202301*7567 = 621944727930768

