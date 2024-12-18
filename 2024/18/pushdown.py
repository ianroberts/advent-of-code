import itertools
from typing import Callable

from aoc_common.grid import Cell
from aoc_common.heapdict import heapdict


valid_rows = valid_cols = range(71)


def load_data():
    droptimes: dict[Cell, int] = {}
    with open("input", "r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                break
            col, row = (int(v) for v in line.split(","))
            droptimes[Cell(row, col)] = i

    return droptimes


def shortest_path(
    start: Cell,
    end: Cell,
    neighbours: Callable[[Cell], list[Cell]],
):
    """
    A* shortest path algorithm, where all edges are equal weight (1).

    :param start: the start node, typically top left in the grid
    :param end: the end node, bottom right in the grid
    :param neighbours: function that takes a Cell and returns its eligible neighbours
    :return: the set of nodes making up a shortest path from start to end
    :raises ValueError: if no path exists from start to end
    """
    open_list = heapdict()
    closed_list: set[Cell] = set()
    f = {}
    g = {}
    pred = {}
    open_list[start] = 0
    f[start] = 0
    g[start] = 0

    while len(open_list):
        node, f_node = open_list.popitem()
        closed_list.add(node)

        if node == end:
            # Reached the goal - trace back through pred links to find the
            # nodes that are part of the shortest path
            path = {node}
            while node in pred:
                node = pred[node]
                path.add(node)
            return path

        for child in neighbours(node):
            if child in closed_list:
                continue
            child_g = g[node] + 1
            if child not in g or child_g < g[child]:
                g[child] = child_g
                pred[child] = node
                # Use manhattan distance to end as heuristic function - we use the
                # fact that the end position is bottom right so we don't need to
                # take any absolute values, end.row-child.row and end.col-child.col
                # are both always >= 0
                f[child] = child_g + end.row - child.row + end.col - child.col
                open_list[child] = f[child]

    # If we reach here we never found a path to the goal
    raise ValueError(f"No path found")


def find_path(droptimes: dict[Cell, int], timestep: int) -> set[Cell]:
    """
    Find a shortest path through the graph as it looks after the given timestep.
    The ``timestep`` is zero based, the first byte drops at timestep zero, the
    second at timestep 1, etc. so the graph we are searching **includes** the
    byte that dropped at ``timestep``.
    :param droptimes: mapping from byte Cell to the timestep on which that byte dropped
    :param timestep: the timestep at which we are simulating
    :return: the ``set`` of cells that are part of the path (we only care later
    on about whether or not a given cell is in the path, not where it was in the order)
    """

    def nbr(node: Cell):
        """
        The valid neighbours of a given cell are those cells that either will never
        contain a dropped byte, or where that byte will drop **after** the target
        timestep
        """
        return [
            c
            for c in node.neighbours(valid_rows, valid_cols)
            if c not in droptimes or droptimes[c] > timestep
        ]

    return shortest_path(Cell(0, 0), Cell(70, 70), nbr)


def part1():
    """
    Find shortest path through the graph whose nodes are the **non-blocked** spaces
    and whose edges are cardinal N/S/E/W directions, starting at the top left and
    finishing at the bottom right.
    """
    droptimes = load_data()

    # "Simulate the first kilobyte" means we want the state of the graph after
    # zero-based timestep 1023
    path = find_path(droptimes, 1023)
    # returned path is the cells, including the start and end, so number of _steps_
    # is one fewer
    print(f"Shortest path in graph after 1024 ns: {len(path) - 1}")


def part2():
    """
    Starting from the 1023 path (which we know exists, given part 1), keep dropping
    blockers one by one.  Whenever a blocker falls on a cell that is part of the
    current shortest path, re-calculate the path given the current timestep.  Stop
    at the first timestep where it is no longer possible to find any path from
    start to end.
    """
    droptimes = load_data()
    path = find_path(droptimes, 1023)
    # I'm making use here of the fact that python dict iteration is guaranteed to
    # be insertion order, so we will definitely step through the items in the same
    # order as they appeared in the input file
    for blocker, timestep in itertools.islice(droptimes.items(), 1024, None):
        if blocker in path:
            try:
                path = find_path(droptimes, timestep)
            except ValueError:
                # No possible path - we are done
                break

    print(f"Found blocking path after {timestep} ns, final blocker at {blocker}")


if __name__ == "__main__":
    part1()
    part2()
