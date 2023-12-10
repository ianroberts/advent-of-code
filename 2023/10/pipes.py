from collections import namedtuple
from typing import TypeVar
T = TypeVar()


class Cell(namedtuple("Cell", ["row", "col"])):
    """
    This is probably overkill for AoC but I used it as an excuse to play with
    operator overloading in Python
    """
    def __add__(self, other: "Cell") -> "Cell":
        """
        Override cell1 + cell2 to do pointwise sum rather than the usual tuple concatenation
        """
        return Cell(self.row + other.row, self.col + other.col)

    def __sub__(self, other: "Cell") -> "Cell":
        """
        Pointwise subtraction
        """
        return Cell(self.row - other.row, self.col - other.col)

    def __neg__(self) -> "Cell":
        return Cell(-self.row, -self.col)

    def of(self, grid: list[list[T]]) -> T:
        """
        Lookup this cell in a 2d grid
        """
        return grid[self.row][self.col]




pipe_types = {
    "|": [Cell(-1, 0), Cell(1, 0)],
    "-": [Cell(0, -1), Cell(0, 1)],
    "L": [Cell(-1, 0), Cell(0, 1)],
    "J": [Cell(-1, 0), Cell(0, -1)],
    "7": [Cell(1, 0), Cell(0, -1)],
    "F": [Cell(1, 0), Cell(0, 1)],
}


# Copied from day 3 - same principle of reading a rectangular matrix and surrounding it
# with a border of dots
def input_matrix() -> list[str]:
    """
    Read the input file, extend any short lines with dots to the length of the longest
    one to make the grid rectangular (this is not actually required for the given
    test data, as that matrix is rectangular to start with), then add a border of dots
    around the outside to avoid any strange edge effects in subsequent analysis.
    """
    with open("input", "r") as f:
        # Add leading and trailing dot to each line
        grid: list[str] = [f".{line.strip()}." for line in f]

    longest_line = max(len(line) for line in grid)
    for i in range(len(grid)):
        if len(grid[i]) < longest_line:
            grid[i] += "." * (longest_line - len(grid[i]))

    # Add "empty" (i.e. all dots) first and last lines to complete the border
    grid.insert(0, "." * longest_line)
    grid.append("." * longest_line)

    return grid


def build_graph(grid: list[str]) -> tuple[list[list[list[Cell]]], Cell]:
    """
    Turn the input representation into a graph where each cell is a list of the coordinates of
    cells to which it is linked
    :param grid: the original grid of symbols
    :return: grid of links
    """
    graph = []
    start_point = None
    for r, row in enumerate(grid):
        graph_row = []
        graph.append(graph_row)
        for c, symbol in enumerate(row):
            cell = Cell(r, c)
            if symbol == "S":
                start_point = cell
            graph_row.append([cell + offset for offset in pipe_types.get(symbol, [])])

    if not start_point:
        raise Exception("No S found in grid")

    # fix up the start cell - look at the four cells around it and determine which ones connect to it
    for neighbour in [Cell(0, -1), Cell(-1, 0), Cell(0, 1), Cell(1, 0)]:
        neighbour_links = (start_point + neighbour).of(graph)
        if start_point in neighbour_links:
            start_point.of(graph).append(start_point + neighbour)

    return graph, start_point


def find_loop(graph: list[list[list[Cell]]], start_point: Cell) -> list[Cell]:
    """
    Find the list of cells that make up the pipe loop from the given start point
    """
    guard = 0
    loop_nodes = [start_point]
    finished = False
    cur_point = start_point
    #print(f"{start_point=}")
    # the last way we moved - we can traverse the loop in either direction so pick one arbitrary
    # entry point to begin
    prev_point = start_point.of(graph)[0]
    while guard < len(graph) * len(graph[0]):
        # possible moves from here are all the outgoing links from cur_point _except_ the one we
        # came in on
        possible_moves = [dest for dest in cur_point.of(graph) if dest != prev_point]
        if not possible_moves:
            raise Exception(f"No legal exit from {cur_point} except by backtracking to {prev_point}")

        prev_point = cur_point
        cur_point = possible_moves[0]
        #print(f"{cur_point=}")

        if cur_point == start_point:
            finished = True
            break
        loop_nodes.append(cur_point)

    if finished:
        return loop_nodes
    else:
        raise Exception("We've covered the whole grid without getting back to where we started...")


def loop_length() -> int:
    graph, start_point = build_graph(input_matrix())
    return len(find_loop(graph, start_point))


def inside_area() -> int:
    grid = input_matrix()
    # print("\n".join(grid))
    graph, start_point = build_graph(grid)
    loop = set(find_loop(graph, start_point))

    # A point is "inside" the loop if any straight line that you draw to it from a point on the edge of
    # the grid crosses the loop an odd number of times.  This is true whatever direction you draw
    # the line, so for simplicity I'll consider the line starting from the beginning of this point's
    # row, so we can process the whole grid element-wise from the top left.
    #
    # We imagine we are walking along the bottom edge of each grid cell, which means that you "cross"
    # the loop whenever you hit any loop cell that has a link to it's neighbour in the next row
    # (i.e. it's either a |, F or 7, or the start point S if it was inferred to be one of those types)
    inside_points = 0
    for r, row in enumerate(graph):
        num_crossings = 0
        for c, neighbours in enumerate(row):
            if Cell(r, c) in loop:
                if Cell(r+1, c) in neighbours:
                    num_crossings += 1
            else:
                # This is not a loop cell, so see whether it's inside or outside
                if num_crossings % 2 == 1:
                    inside_points += 1

    return inside_points


if __name__ == "__main__":
    # loop is always an even number of steps since to get back to where you started, for every row you
    # go up you must come back down, and for every column you step right you must step left.  So the
    # furthest point is always half the total length of the loop
    print(f"Furthest point of the loop from start is {loop_length()//2}")
    print(f"Number of cells inside the loop: {inside_area()}")
