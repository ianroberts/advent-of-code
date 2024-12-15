import operator

from aoc_common.grid import Cell, Direction

GET_ROW = operator.attrgetter("row")


def load_data():
    with open("input", "r") as f:
        grid = []
        start_pos = None
        for row, line in enumerate(f):
            line = (
                line.strip()
                .replace("#", "##")
                .replace(".", "..")
                .replace("O", "[]")
                .replace("@", "@.")
            )
            if line == "":
                break
            if (col := line.find("@")) >= 0:
                line = line.replace("@", ".")
                start_pos = Cell(row, col)

            grid.append([ch for ch in line])

        # rest of the file is the moves
        moves = "".join(line.strip() for line in f)

    return grid, start_pos, moves


def try_move_horizontal(grid: list[list[str]], direction: Cell, start: Cell) -> bool:
    """
    Try and move one step in an E/W direction in the grid, pushing any boxes that can
    be moved.

    :param grid: the grid, which will be mutated if the move pushes any boxes
    :param direction: Cell representing a vector for the move direction
    :param start: start position of the move
    :return: True if the robot was able to move from this position, False if it was blocked
    (either directly by a wall, or by a stack of boxes up against a wall).
    """
    cells_to_move = 0
    while True:
        item = (start + (cells_to_move + 1) * direction).of(grid)
        if item in "[]":
            cells_to_move += 2
        elif item == "#":
            # blocked
            return False
        else:
            # found a space after a stack of zero or more boxes
            break

    # push the stack, if there is one - to push a stack of N cells, set cell N+1 to
    # the current value of N, N to the current N-1, etc.
    stack_end = start + cells_to_move * direction
    for n in range(cells_to_move + 1):
        (stack_end + direction).set(grid, stack_end.of(grid))
        stack_end -= direction

    return True


def try_move_vertical(grid: list[list[str]], direction: Cell, start: Cell) -> bool:
    """
    Try and move one step in a N/S direction in the grid, pushing any boxes that can
    be moved.

    :param grid: the grid, which will be mutated if the move pushes any boxes
    :param direction: Cell representing a vector for the move direction
    :param start: start position of the move
    :return: True if the robot was able to move from this position, False if it was blocked
    (either directly by a wall, or by a tree of box stacks that hits a wall).
    """
    # this time we need to keep track of the actual cells being moved, not just how many of them
    cells_to_move = {start}
    # cells to be moved in the row we most recently inspected
    prev_row_cells_to_move = {start}
    while len(prev_row_cells_to_move) > 0:
        # Each time round this loop we take the positions of the boxes that would be moved
        # from the previous row, and see what is in front of them.  If any of them are
        # blocked by a wall then the whole move operation fails.  If there is nothing
        # in front of any of them then the complete set of boxes to move has been
        # computed and the loop ends.  Otherwise the cells in front of the previous row
        # include one or more boxes, so repeat the loop with the set of cells covered by
        # those boxes.
        this_row = set()
        for c in prev_row_cells_to_move:
            next_cell = c + direction
            if next_cell.of(grid) == "#":
                # We have hit a wall, so nothing can move
                return False
            if next_cell.of(grid) == "[":
                this_row.add(next_cell)
                # and the other half of the box!
                this_row.add(next_cell + Direction.EAST)
            elif next_cell.of(grid) == "]":
                this_row.add(next_cell)
                # and the other half of the box!
                this_row.add(next_cell + Direction.WEST)
            # else it's a gap - nothing to do

        # advance by one row
        cells_to_move.update(this_row)
        prev_row_cells_to_move = this_row

    # If we get here, we found enough space to move things, so now move them.
    # Sort the set of cells so that we start with the ones furthest from the
    # start point and work inwards towards the start point
    sorted_cells = sorted(cells_to_move, key=GET_ROW, reverse=direction.row > 0)
    for c in sorted_cells:
        (c + direction).set(grid, c.of(grid))
        # Leave a space behind - this may or may not get filled in when we
        # start processing the next row back, depending what caused this cell
        # to move in the first place.
        c.set(grid, ".")

    return True


MOVE = {
    ">": (Direction.EAST, try_move_horizontal),
    "v": (Direction.SOUTH, try_move_vertical),
    "<": (Direction.WEST, try_move_horizontal),
    "^": (Direction.NORTH, try_move_vertical),
}


def predict_position():
    grid, robot_pos, moves = load_data()
    for m in moves:
        d, try_move = MOVE[m]
        if try_move(grid, d, robot_pos):
            robot_pos += d

    print("\n".join("".join(c for c in line) for line in grid))

    total = sum(
        (100 * r + c) if grid[r][c] == "[" else 0
        for r in range(len(grid))
        for c in range(len(grid[0]))
    )
    print(f"Sum of box coords: {total}")


if __name__ == "__main__":
    predict_position()
