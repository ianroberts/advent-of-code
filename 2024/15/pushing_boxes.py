from aoc_common.grid import Cell, Direction


def load_data():
    with open("input", "r") as f:
        grid = []
        start_pos = None
        for row, line in enumerate(f):
            line = line.strip()
            if line == "":
                break
            if (col := line.find("@")) >= 0:
                line = line.replace("@", ".")
                start_pos = Cell(row, col)

            grid.append([ch for ch in line])

        # rest of the file is the moves
        moves = "".join(line.strip() for line in f)

    return grid, start_pos, moves


MOVE_DIRECTIONS = {
    ">": Direction.EAST,
    "v": Direction.SOUTH,
    "<": Direction.WEST,
    "^": Direction.NORTH,
}


def try_move(grid: list[list[str]], direction: Cell, start: Cell) -> bool:
    """
    Try and move one step in a direction in the grid, pushing any boxes that can
    be moved.

    :param grid: the grid, which will be mutated if the move pushes any boxes
    :param direction: Cell representing a vector for the move direction
    :param start: start position of the move, in the coordinate system of the move direction
    :return: True if the robot was able to move from this position, False if it was blocked
    (either directly by a wall, or by a stack of boxes).
    """
    boxes_to_move = 0
    while True:
        item = (start + (boxes_to_move + 1) * direction).of(grid)
        if item == "O":
            boxes_to_move += 1
        elif item == "#":
            # blocked
            return False
        else:
            # found a space after a stack of zero or more boxes
            break

    if boxes_to_move:
        # push the stack - this effectively means turning the box immediately after
        # the start point to a space, and the space after the current stack to a box
        (start + direction).set(grid, ".")
        (start + (boxes_to_move + 1) * direction).set(grid, "O")

    return True


def predict_position():
    grid, robot_pos, moves = load_data()
    for m in moves:
        d = MOVE_DIRECTIONS[m]
        if try_move(grid, d, robot_pos):
            robot_pos += d

    print("\n".join("".join(c for c in line) for line in grid))

    print(f"Sum of box coords: {sum((100 * r + c) if grid[r][c] == 'O' else 0 for r in range(len(grid)) for c in range(len(grid[0])))}")


if __name__ == "__main__":
    predict_position()