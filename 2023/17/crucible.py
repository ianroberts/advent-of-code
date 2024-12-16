from aoc_common.heapdict import heapdict
from collections import namedtuple


with open("input", "r") as f:
    MATRIX = [[int(i) for i in line.strip()] for line in f]

ROWS = len(MATRIX)
COLS = len(MATRIX[0])

# Constants for axes
EW, NS = 0, 1


class Node(namedtuple("Node", ["row", "col", "axis"])):
    """
    A Node in the graph, consisting of the row and column and the axis on which
    the cell was approached - the next move must be on the other axis
    """

    def neighbours(self, minsteps, maxsteps):
        """
        Generate all possible neighbour nodes of this one, along with their respective costs.
        A "neighbour" is a node between minsteps and maxsteps (inclusive) cells away from this
        one in each direction on the other axis, and the associated cost is the sum of the
        costs of all cells between this one and the neighbour.
        """
        if self.row == ROWS-1 and self.col == COLS-1:
            yield END, 0
            return

        for n in range(minsteps, maxsteps+1):
            # I'm using != NS rather than == EW to let the top left start node have
            # neighbours on both axes (to the right *and* below)
            if self.axis != NS:
                if self.row >= n:  # Don't go beyond the edge of the matrix
                    yield (
                        Node(self.row-n, self.col, NS),
                        sum(MATRIX[r][self.col] for r in range(self.row-n, self.row))
                    )
                if self.row < ROWS-n:
                    yield (
                        Node(self.row+n, self.col, NS),
                        sum(MATRIX[r][self.col] for r in range(self.row+1, self.row+n+1))
                    )

            if self.axis != EW:
                if self.col >= n:
                    yield (
                        Node(self.row, self.col-n, EW),
                        sum(MATRIX[self.row][c] for c in range(self.col-n, self.col))
                    )
                if self.col < COLS-n:
                    yield (
                        Node(self.row, self.col+n, EW),
                        sum(MATRIX[self.row][c] for c in range(self.col+1, self.col+n+1))
                    )


# Special node representing the origin, with None for its axis so it can have neighbours both ways
START = Node(0, 0, None)

# Special END node representing the destination, that is zero cost away from both of the bottom
# right corner nodes (one for the approach from above, one for the approach from the left)
END = Node(ROWS, COLS, None)


def cheapest_path(minsteps: int, maxsteps: int):
    open_list = heapdict()
    closed_list: set[Node] = set()
    f = {}
    g = {}
    open_list[START] = 0
    f[START] = 0
    g[START] = 0

    while len(open_list):
        node, f_node = open_list.popitem()
        closed_list.add(node)

        if node == END:
            # Reached the goal - return the cost of the shortest path
            return g[node]

        for child, cost in node.neighbours(minsteps, maxsteps):
            if child in closed_list:
                continue
            child_g = g[node] + cost
            if child not in g or child_g < g[child]:
                g[child] = child_g
                # Use manhattan distance to goal as heuristic function
                f[child] = child_g + END.row - child.row + END.col - child.col
                open_list[child] = f[child]

    # If we reach here we never found a path to the goal
    raise ValueError(f"No path from {START} to {END}")


if __name__ == "__main__":
    print(f"Cheapest path from {START} to {END} for small crucibles (1-3 steps) "
          f"costs {cheapest_path(1, 3)}")
    print(f"Cheapest path from {START} to {END} for ultra crucibles (4-10 steps) "
          f"costs {cheapest_path(4, 10)}")
