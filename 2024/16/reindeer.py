from collections import namedtuple, defaultdict

from aoc_common.grid import Cell, Direction
from aoc_common.heapdict import heapdict

# Each cell in our grid maps to _two_ nodes in the graph, one for
# when the cell is approached from the north or south ("vertical")
# and one for when the cell is approached from the east or west
# ("horizontal").  Two axes are sufficient, we don't need to track
# all four possible approach directions separately because all 90
# degree turns have the same cost, we only care about cheapest-cost
# paths, and a path that loops round on itself will never be cheaper
# than one that doesn't (turning right once will always be cheaper
# than turning left three times).
Node = namedtuple("Node", ["c", "axis"])


def load_data():
    # parse the input file, converting the S and E to dots but remembering
    # their locations
    with open("input", "r") as f:
        grid = []
        for r, l in enumerate(f):
            l = l.strip()
            s = l.find("S")
            if s >= 0:
                start_node = Node(Cell(r, s), "h")
                l = l[:s] + "." + l[s + 1 :]

            e = l.find("E")
            if e >= 0:
                end_cell = Cell(r, e)
                l = l[:e] + "." + l[e + 1 :]

            grid.append(l)

    nodes: set[Node] = set()
    # neighbours maps each Node to its set of (neighbour-node, cost) tuples
    neighbours: dict[Node, set[tuple[Node, int]]] = defaultdict(set)

    # First find the cells that are eligible to be nodes in the graph,
    # which means (a) the start, (b) the end, and (c) any "." that has
    # at least one north or south "." neighbour AND at least one east
    # or west neighbour - this covers the corners and junctions.
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "#":
                # Walls can never be nodes
                continue

            cell = Cell(r, c)

            is_node = (cell == start_node.c or cell == end_cell) or (
                (
                    (cell + Direction.NORTH).of(grid) == "."
                    or (cell + Direction.SOUTH).of(grid) == "."
                )
                and (
                    (cell + Direction.WEST).of(grid) == "."
                    or (cell + Direction.EAST).of(grid) == "."
                )
            )

            if not is_node:
                continue

            # This cell is eligible, create two graph nodes for this cell,
            # one for the vertical and one for the horizontal axis
            h_node = Node(cell, "h")
            v_node = Node(cell, "v")
            nodes.add(h_node)
            nodes.add(v_node)
            # and make each a neighbour of the other at cost 1000 to
            # represent the cost of turning 90 degrees either way
            neighbours[h_node].add((v_node, 1000))
            neighbours[v_node].add((h_node, 1000))

    # Now link up adjacent nodes along their straight paths.  Two nodes
    # are adjacent if they are in the same orientation (h or v) and all
    # the intervening characters between their positions in the grid are
    # dots, and the cost of that edge is the number of steps.
    for n in nodes:
        for d in Direction.HORIZONTAL if n.axis == "h" else Direction.VERTICAL:
            cell = n.c
            nbr = None
            found_nbr = False
            distance = 0
            # Walk in a straight line until we hit either another node or
            # a wall
            while cell.of(grid) == ".":
                cell = cell + d
                distance += 1
                if (nbr := Node(cell, n.axis)) in nodes:
                    found_nbr = True
                    break

            if found_nbr:
                neighbours[n].add((nbr, distance))
                neighbours[nbr].add((n, distance))

    # Special end node that is zero cost away from both axes of the end cell,
    # so that paths approaching the end cell from either axis will be equally
    # cheap, all other things being equal
    end_node = Node(end_cell, None)
    neighbours[Node(end_cell, "h")].add((end_node, 0))
    neighbours[Node(end_cell, "v")].add((end_node, 0))

    return grid, start_node, end_node, neighbours


def cheapest_path():
    grid, start_node, end_node, neighbours = load_data()

    # Dijkstra to find all the shortest paths from start_node to... well,
    # anywhere, but we only care about paths to the end node

    # Use a heapdict for the unvisited list so the next node to be processed
    # is always the one with the lowest cost path from the start
    open_list = heapdict()
    # closed_list is the set of nodes we have completely visited
    closed_list: set[Node] = set()
    # for each node visited, track the set of its lowest-cost immediate
    # predecessors in the path from start - most of the time this will
    # be one node, but it might be more than one if there are multiple
    # paths to this node via different but equally cheap routes
    predecessors: dict[Node, set[Node]] = {}
    # costs is the total cost of the cheapest path so far found to each node
    # (including the fully visited ones)
    costs: dict[Node, int] = {}

    # Initial conditions - we're starting from the start node, and its
    # distance from the start node is (obviously) zero
    open_list[start_node] = 0
    costs[start_node] = 0

    while len(open_list):
        node, dist_node = open_list.popitem()
        closed_list.add(node)

        for child, cost in neighbours[node]:
            if child in closed_list:
                continue
            child_cost = costs[node] + cost
            if child_cost <= costs.get(child, 10000000000000):
                if child_cost == costs.get(child):
                    # an alternative path to this child that is the same cost as
                    # the cheapest we've found so far
                    predecessors[child].add(node)
                else:
                    # either a cheaper path than we previously found, or a node
                    # we've not seen before
                    costs[child] = child_cost
                    predecessors[child] = {node}
                open_list[child] = costs.get(child, 10000000000000)

    if end_node not in costs:
        # we never found a path to the goal
        raise ValueError(f"No path from {start_node} to {end_node}")

    print(f"Cheapest path cost = {costs[end_node]}")

    # now walk back along the predecessor chain from the end node and record
    # all the cells that any of the cheapest paths touch
    frontier = {end_node}
    covered_cells = set()
    while frontier:
        n = frontier.pop()
        covered_cells.add(n.c)
        for p in predecessors.get(n, ()):
            frontier.add(p)
            # vector is the offset to move from the cell of node n to the
            # cell of node p - vector.row and vector.col cannot both be
            # non-zero, negative numbers mean moving up or left, positive
            # is down or right
            vector: Cell = p.c - n.c
            if vector.row != 0:
                delta = 1 if vector.row > 0 else -1
                for i in range(delta, vector.row, delta):
                    covered_cells.add(Cell(n.c.row + i, n.c.col))
            if vector.col != 0:
                delta = 1 if vector.col > 0 else -1
                for i in range(delta, vector.col, delta):
                    covered_cells.add(Cell(n.c.row, n.c.col + i))

    # Draw all the cheapest paths, for sanity check
    print(
        "\n".join(
            "".join(
                ("x" if Cell(r, c) in covered_cells else ch)
                for c, ch in enumerate(line)
            )
            for r, line in enumerate(grid)
        )
    )

    print(f"Tiles touched by a cheapest path: {len(covered_cells)}")


if __name__ == "__main__":
    cheapest_path()
