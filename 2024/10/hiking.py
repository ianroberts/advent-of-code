from aoc_common.grid import Cell


def load_data():
    with open("input", "r") as f:
        return [[int(c) for c in l.strip()] for l in f]


def trails():
    grid = load_data()

    # build a directed graph where the nodes are grid cells and the edges link
    # cell A to any neighbouring cell B which is one unit *downhill*.  So 9s
    # link to adjacent 8s, 8s to 7s, etc.
    links: list[list[set[Cell]]] = [[set() for _ in row] for row in grid]

    # Also track which cells contain a 9 and which contain a 0, as we'll need
    # those later
    zeros = []
    nines = []

    valid_rows = range(len(grid))
    valid_cols = range(len(grid[0]))
    for c in (Cell(r, c) for r in valid_rows for c in valid_cols):
        val = c.of(grid)
        if val == 9:
            nines.append(c)
        if val == 0:
            zeros.append(c)
        c.of(links).update(n for n in c.neighbours(valid_rows, valid_cols) if n.of(grid) == val - 1)

    # part 1 - sum up how many nines are reachable (in any way) from each zero.
    # reachable_nines will contain, for each cell, the set of distinct "9" cells
    # from which this cell can be reached by a path through the graph.  Initially
    # this is a singleton set of the cell itself if the cell value is 9, otherwise
    # an empty set.
    reachable_nines: list[list[set[Cell]]] = [
        [({Cell(row, col)} if Cell(row, col).of(grid) == 9 else set()) for col in valid_cols] for row in valid_rows
    ]
    # part 2 - find the number of distinct paths from each zero to each nine
    # routes_to_nine will contain, for each cell, the set of distinct paths
    # between that cell and a cell containing 9.  Each path is represented as
    # a tuple of Cells, starting with this cell and running uphill to a 9.
    # Initially this is a singleton set of a one-step path to this cell if the
    # cell value is 9, else an empty set
    routes_to_nine: list[list[set[tuple[Cell]]]] = [
        [({(Cell(row, col),)} if Cell(row, col).of(grid) == 9 else set()) for col in valid_cols] for row in valid_rows
    ]

    # start from the nines
    frontier = set(nines)
    # The traversal will end when we run out of nodes - we don't need to keep a
    # visited list because the graph is acyclic by definition (all edges point
    # "downhill")
    while frontier:
        c = frontier.pop()
        # for each adjacent (downhill) cell
        for n in c.of(links):
            # the downhill cell has a path to each nine reachable from the node we came from
            n.of(reachable_nines).update(c.of(reachable_nines))
            n.of(routes_to_nine).update((n, *route) for route in c.of(routes_to_nine))
            # continue searching from this node
            frontier.add(n)

    print(f"Trail total score: {sum(len(c.of(reachable_nines)) for c in zeros)}")
    print(f"Trail total rating: {sum(len(c.of(routes_to_nine)) for c in zeros)}")


if __name__ == "__main__":
    trails()
