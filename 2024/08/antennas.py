import math
from collections import namedtuple, defaultdict
from itertools import combinations

import numpy as np


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

    def __floordiv__(self, other: int) -> "Cell":
        """
        Divide each coordinate by the given number
        """
        return Cell(self.row // other, self.col // other)

    def __neg__(self) -> "Cell":
        return Cell(-self.row, -self.col)


# There are a maximum of 62 distinct antenna types (26 lowercase, 26 uppercase,
# 10 digit), so we can represent each type as a single bit in a 64 bit flag
ANTENNA_TYPES = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def load_data():
    with open("input", "r") as f:
        lines = [l.strip() for l in f]

    antennas = defaultdict(set)

    for row, l in enumerate(lines):
        for col, ch in enumerate(l):
            if ch != ".":
                antennas[ch].add(Cell(row, col))

    nodes = np.zeros((len(lines), len(lines[0])), np.int64)
    return antennas, nodes


def anti_nodes_simple():
    antennas, nodes = load_data()
    valid_rows = range(nodes.shape[0])
    valid_cols = range(nodes.shape[1])

    for ch, cells in antennas.items():
        freq = 2**ANTENNA_TYPES.find(ch)
        for a1, a2 in combinations(cells, 2):
            vec = a2 - a1
            for node in (a1 - vec, a2 + vec):
                if node.row in valid_rows and node.col in valid_cols:
                    nodes[node] |= freq

    print(f"Number of anti-nodes: {np.count_nonzero(nodes)}")


def anti_nodes_all():
    antennas, nodes = load_data()
    valid_rows = range(nodes.shape[0])
    valid_cols = range(nodes.shape[1])

    for ch, cells in antennas.items():
        freq = 2**ANTENNA_TYPES.find(ch)
        for a1, a2 in combinations(cells, 2):
            vec = a2 - a1
            # This time distance is not a factor, so if the coordinates of
            # the vector from a1 to a2 have a common divisor then we must
            # scale down the vector by that amount, since the intervening
            # cells at those places will also be "in line with two antennas".
            # For example, if the vector a1->a2 is (10, 5) then the points
            # at (2, 1), (4, 2), (6, 3) and (8, 4) will also be exactly in line
            scale = math.gcd(*vec)
            vec //= scale

            # Now start from a1 and put antinodes at all integer multiples of
            # the scaled vector (positive and negative) until we fall off the
            # edge of the map.
            c1 = a1
            c2 = a1
            # remember a1 is itself an antinode
            nodes[a1] |= freq
            keep_going = True
            while keep_going:
                keep_going = False
                c1 = c1 + vec
                c2 = c2 - vec
                for node in (c1, c2):
                    if node.row in valid_rows and node.col in valid_cols:
                        keep_going = True
                        nodes[node] |= freq

    print(f"Number of anti-nodes with harmonics: {np.count_nonzero(nodes)}")


if __name__ == "__main__":
    anti_nodes_simple()
    anti_nodes_all()