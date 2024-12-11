from collections import namedtuple
from typing import TypeVar, Sequence, MutableSequence

T = TypeVar("T")


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

    def of(self, grid: Sequence[Sequence[T]]) -> T:
        return grid[self.row][self.col]

    def set(self, grid: Sequence[MutableSequence[T]], val: T) -> None:
        grid[self.row][self.col] = val

    def neighbours(self, valid_rows, valid_cols, include_diagonal=False) -> list["Cell"]:
        result = []
        for d in (Direction.DIAGONAL if include_diagonal else Direction.STRAIGHT):
            nbr = self + d
            if nbr.row in valid_rows and nbr.col in valid_cols:
                result.append(nbr)

        return result


class Direction:
    NORTH = Cell(-1, 0)
    NE = Cell(-1, 1)
    EAST = Cell(0, 1)
    SE = Cell(1, 1)
    SOUTH = Cell(1, 0)
    SW = Cell(1,-1)
    WEST = Cell(0, -1)
    NW = Cell(-1, -1)

    STRAIGHT = [EAST, SOUTH, WEST, NORTH]
    DIAGONAL = [EAST, SE, SOUTH, SW, WEST, NW, NORTH, NE]