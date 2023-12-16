from collections import namedtuple

# Constants for the directions
R, D, L, U = range(4)

with open("input", "r") as f:
    LINES = [line.strip() for line in f]
ROWS = len(LINES)
COLS = len(LINES[0])


class Cell(namedtuple("Cell", ["row", "col"])):
    """
    Methods to return neighbour nodes in each direction (assuming the beam will be travelling
    in that direction once it arrives at the neighbour), but only if we are not already at the
    relevant edge of the grid.  E.g. if you try to go right from the right edge the method will
    return None instead of a new node
    """
    def right(self):
        if self.col < COLS - 1:
            return Cell(self.row, self.col+1), R

    def down(self):
        if self.row < ROWS - 1:
            return Cell(self.row+1, self.col), D

    def left(self):
        if self.col > 0:
            return Cell(self.row, self.col-1), L

    def up(self):
        if self.row > 0:
            return Cell(self.row-1, self.col), U


def drop_none(*seq):
    """
    Returns a list of all the non-None positional arguments passed in.
    If all arguments are None the resulting list will be empty.
    """
    return [item for item in seq if item is not None]


def build_graph():

    # This is a graph traversal problem to find all the visited nodes from each start point.
    # The twist is that each cell in the input matrix actually corresponds to *four* nodes
    # in the graph for the four different directions the beam can be travelling on entry
    # to that cell.  So the graph representation is a dict where the key is a (cell, direction)
    # pair and the value is the pairs (neighbour_cell, new_direction) of the cells into which
    # the beam goes and the direction it will be travelling when it gets there.
    graph: dict[tuple[Cell, int], list[tuple[Cell, int]]] = {}

    for r, row in enumerate(LINES):
        for c, char in enumerate(row):
            cell = Cell(r, c)
            if char == ".":
                # continue in the same direction
                graph[(cell, R)] = drop_none(cell.right())
                graph[(cell, D)] = drop_none(cell.down())
                graph[(cell, L)] = drop_none(cell.left())
                graph[(cell, U)] = drop_none(cell.up())
            elif char == "/":
                # turn 90 degrees
                graph[(cell, R)] = drop_none(cell.up())
                graph[(cell, D)] = drop_none(cell.left())
                graph[(cell, L)] = drop_none(cell.down())
                graph[(cell, U)] = drop_none(cell.right())
            elif char == "\\":
                # turn 90 degrees
                graph[(cell, R)] = drop_none(cell.down())
                graph[(cell, D)] = drop_none(cell.right())
                graph[(cell, L)] = drop_none(cell.up())
                graph[(cell, U)] = drop_none(cell.left())
            elif char == "-":
                # left <-> right straight through, U/D go both L & R
                graph[(cell, R)] = drop_none(cell.right())
                graph[(cell, D)] = drop_none(cell.left(), cell.right())
                graph[(cell, L)] = drop_none(cell.left())
                graph[(cell, U)] = drop_none(cell.left(), cell.right())
            elif char == "|":
                # up <-> down straight through, L/R go both U & D
                graph[(cell, R)] = drop_none(cell.up(), cell.down())
                graph[(cell, D)] = drop_none(cell.down())
                graph[(cell, L)] = drop_none(cell.up(), cell.down())
                graph[(cell, U)] = drop_none(cell.up())
            else:
                raise ValueError("Unexpected character in grid")

    return graph


def energized_tiles(graph, start_pos):
    # depth first search to find coverage
    stack = [start_pos]
    # the nodes we have seen (including the start point)
    seen_nodes = set(stack)
    while stack:
        node = stack.pop()
        for neighbour in graph[node]:
            if neighbour not in seen_nodes:
                seen_nodes.add(neighbour)
                stack.append(neighbour)

    # Stack empty - we've covered all reachable nodes.  Now the set of energized tiles
    # will be the *unique Cells* in the seen_nodes set, ignoring the direction flags.
    return len(set(c for c, _ in seen_nodes))


def max_energized(*start_pos):
    graph = build_graph()
    if not start_pos:
        # No start_pos specified, try all the possible edge nodes in their
        # respective directions
        start_pos = []
        start_pos.extend((Cell(r, 0), R) for r in range(ROWS))
        start_pos.extend((Cell(r, COLS-1), L) for r in range(ROWS))
        start_pos.extend((Cell(0, c), D) for c in range(COLS))
        start_pos.extend((Cell(ROWS-1, c), U) for c in range(COLS))

    return max(energized_tiles(graph, pos) for pos in start_pos)


if __name__ == "__main__":
    print(f"Count of energized tiles from (0, 0) -> R: {max_energized((Cell(0, 0), R))}")
    print(f"Maximum energized tiles for any start position: {max_energized()}")
