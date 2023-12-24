from collections import namedtuple

# Part 1 - downhill only
E_NBR = [".", ">"]
S_NBR = [".", "v"]
W_NBR = [".", "<"]
N_NBR = [".", "^"]

# Part 2 - any slope - comment out the above definitions and uncomment these instead
# E_NBR = S_NBR = W_NBR = N_NBR = [".", "^", ">", "v", "<"]


class Cell(namedtuple("Cell", ["row", "col"])):
    def neighbours(self, matrix):
        nbr = []
        if self.row > 0 and matrix[self.row-1][self.col] in N_NBR:
            nbr.append(Cell(self.row-1, self.col))
        if self.row < len(matrix)-1 and matrix[self.row+1][self.col] in S_NBR:
            nbr.append(Cell(self.row+1, self.col))

        # don't need to bounds-check for col as this will never be called on
        # cells in the first or last columns
        if matrix[self.row][self.col-1] in W_NBR:
            nbr.append(Cell(self.row, self.col-1))
        if matrix[self.row][self.col+1] in E_NBR:
            nbr.append(Cell(self.row, self.col+1))

        return nbr


def parse_input():
    """
    Parse the input file to build a graph structure.  The nodes in the graph are:
    - the start cell
    - the end cell
    - each "decision" point, i.e. any cell that is not a # and has *more than two*
      adjacent (up, down, left or right) cells that also aren't #

    The edges link nodes that are reachable by a linear path that does not pass through
    any other junctions, and the weight of each edge is the number of steps along that path.

    :return: a tuple of (list of nodes, dict of edges, start node, end node)
    """

    with open("input", "r") as f:
        matrix = [l.strip() for l in f]

    # special properties of the input:
    # 1. the paths are linear (albeit folded) up to a decision point - no 2x2 or larger tiles
    #    of dots, i.e. in every 2x2 square at least one of the characters _must_ be a "#"
    # 2. slopes only exist adjacent to decision points
    # 3. every possible exit from every decision point is a slope
    # 4. the outside border is solid # except the entry and exit points
    # 5. In fact, looking at the viz, this means the part 1 graph is a perfect acyclic lattice
    #    with all links going left to right, N nodes in each layer, and node i in each layer
    #    connected to or from nodes i and i+1 in the adjacent layer (see hiking-trails.drawio.svg):
    #
    #    start --> N=2 --> 3 --> 4 --> 5 --> 4 --> 5 --> 4 --> 3 --> 2 --> end

    # Graph nodes will be the start and end points
    start = Cell(0, 1)
    end = Cell(len(matrix) - 1, len(matrix[-1]) - 2)
    nodes: list[Cell] = [start, end]

    # plus all the decision points
    for r in range(1, len(matrix)-1):
        for c in range(1, len(matrix[0])-1):
            if (
                    matrix[r][c] != "#" and
                    f"{matrix[r-1][c]}{matrix[r+1][c]}{matrix[r][c-1]}{matrix[r][c+1]}".count("#") < 2
            ):
                # this is a decision point
                nodes.append(Cell(r, c))

    # print out the graph in Mermaid format so I can easily visualise it on draw.io
    print("graph LR")
    for node in nodes:
        print(f"    {node.row}_{node.col}[{node.row}, {node.col}]")

    # to find the edges, start from each node and find each available outgoing direction (either a dot
    # or a downhill slope), and follow that way until we hit either an un-traversable slope (in which
    # case the edge is not valid) or another node (in which case we connect the two).
    #
    # edges is a mapping from origin cell to a list of (dest_cell, edge_weight) pairs
    edges: dict[Cell, list[tuple[Cell, int]]] = {}
    for node in nodes:
        out_edges = []
        if node == end:
            # end node has no out edges
            edges[node] = out_edges
            continue

        out_cells = node.neighbours(matrix)
        for cell in out_cells:
            # follow the path from cell to the next decision node, if there is one
            path_len = 1  # we've already made one step, from "node" to "cell"
            prev_cell = node
            while cell not in nodes:
                path_len += 1
                next_cells = cell.neighbours(matrix)
                try:
                    next_cells.remove(prev_cell)
                except ValueError:
                    # prev_cell was not in next_cells - that's fine
                    pass
                if not next_cells:
                    # this is an invalid path, it either dead-ends or has hit an uphill slope
                    break
                prev_cell = cell
                cell = next_cells[0]  # There will only be one of these as cell is not a decision node
            else:
                # This is a weird python thing - in a while ... else the else block only runs if
                # the while terminates normally, not if it terminates with a break
                out_edges.append((cell, path_len))

        edges[node] = out_edges

    for n, out in edges.items():
        for dest, weight in out:
            print(f"    {n.row}_{n.col} -- {weight} --> {dest.row}_{dest.col}")

    return nodes, edges, start, end


def find_longest_path():
    nodes, edges, start, end = parse_input()

    def find_longest(cur_weight: int, cur_path: list[Cell]) -> tuple[int, list[Cell]]:
        """
        Recursive function that takes a "path so far" and finds the longest extension of
        that path to the end node that does not touch any nodes already visited.
        :param cur_weight: the cumulative weight of the edges traversed in that path
        :param cur_path: the path taken so far to reach the current node
        :return: the weight and node list of the longest path from start to end that starts
        with the given prefix
        """
        if cur_path[-1] == end:
            # Reached the destination
            return cur_weight, cur_path
        else:
            # find the longest path from each of the not-yet-visited neighbours of the
            # current endpoint, and choose the longest out of those.  If any of the
            # neighbours would result in a path that can never reach the end node, then
            # the recursive find_longest call will ultimately return a zero weight, and
            # will thus be pruned later in the search as it'll never be the longest option.
            max_weight = 0
            longest = None
            for n, nbr_weight in edges[cur_path[-1]]:
                if n not in cur_path:
                    w, lp = find_longest(cur_weight+nbr_weight, cur_path + [n])
                    if w > max_weight:
                        longest = lp
                        max_weight = w
            return max_weight, longest

    return find_longest(0, [start])


if __name__ == "__main__":
    print(f"max path weights: {find_longest_path()}")
