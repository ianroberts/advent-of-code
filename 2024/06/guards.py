import numpy as np

# We will represent the state of each grid square by a bitmap representing
# which directions the guard has ever been facing on that square.  I've chosen
# the mask so that turning right from any direction is a right rotation of the
# 4 bit number, and turning left is a left rotation.
EAST = 8
SOUTH = 4
WEST = 2
NORTH = 1

# Blocked squares are represented by numbers < 0
BLOCKED = -1


def load_data():
    start_row = -1
    start_col = -1
    grid = []
    with open("input", "r") as f:
        for nrow, line in enumerate(f):
            line = line.strip()
            row = []
            for ncol, ch in enumerate(line):
                match ch:
                    case "#":
                        row.append(BLOCKED)
                    case "^":
                        start_row, start_col = nrow, ncol
                        # This square has already been visited facing north
                        row.append(NORTH)
                    case _:
                        row.append(0)

            grid.append(row)
    return np.array(grid, np.int8), start_row, start_col


def turn_right(dir: int) -> int:
    """
    Turn 90 degrees right from the given direction.
    """
    if dir == NORTH:
        return EAST

    return dir >> 1


def move(direction, row, col):
    """
    Compute the new row and column coordinates that result from taking one step
    in the given direction.
    """
    if direction == NORTH:
        return row - 1, col
    if direction == EAST:
        return row, col + 1
    if direction == SOUTH:
        return row + 1, col

    return row, col - 1


def walk(grid: np.ndarray, test_loop: bool, row, col, direction):
    """
    Walk the grid from a given starting state and position to determine whether
    the current walk will end in a loop or in an exit off the side of the grid.

    :param grid: the 2d array of grid cells, each cell being a number -1 if
    the cell is an obstruction, else a four bit bitmap recording the directions
    in which the current walk has already traversed this cell.
    :param test_loop: if true, at every point where the walk proceeds ahead
    into a previously unvisited cell, make a clone of the grid with that
    unvisited cell replaced by an obstruction and recursively walk that clone
    to determine whether adding an obstruction there would cause a loop.  Print
    the total number of such cells at the end.
    :param row: the row position at which the walk starts
    :param col: the column position at which the walk starts
    :param direction: the direction the guard is facing at the start of the walk
    :return: True if the walk results in a loop (arriving at a cell that has
    already been visited while travelling in the current direction), False if it
    ends by walking off the side of the grid.
    """
    valid_rows = range(grid.shape[0])
    valid_cols = range(grid.shape[1])
    loop_obstructions = 0

    while True:
        new_row, new_col = move(direction, row, col)
        if new_row not in valid_rows or new_col not in valid_cols:
            # We have left the grid
            break

        if grid[new_row, new_col] == BLOCKED:
            turn_direction = turn_right(direction)
            # Need to turn
            if (grid[row, col] & turn_direction) != 0:
                # we have been here before
                return True
            else:
                # we have not been here before, so continue exploring
                grid[row, col] |= turn_direction
                direction = turn_direction
        else:
            if test_loop and grid[new_row, new_col] == 0:
                # the place we would move to has not been visited before,
                # see whether it would cause a loop if we were to put an
                # obstruction there instead of an empty space
                test_grid = grid.copy()
                test_grid[new_row, new_col] = BLOCKED
                if walk(test_grid, False, row, col, direction):
                    loop_obstructions += 1

            # keep going in the same direction
            grid[new_row, new_col] |= direction
            row, col = new_row, new_col

    if test_loop:
        print(f"Number of obstructions that would create a loop: {loop_obstructions}")

    return False


def covered_area():
    grid, start_row, start_col = load_data()

    walk(grid, True, start_row, start_col, NORTH)

    # At the end of the walk, visited cells are those whose value is not 0 (empty)
    # or -1 (obstructed)
    num_visited = sum(1 if cell > 0 else 0 for row in grid for cell in row)

    # debug - print the grid with obstructions as # and visited cells as X
    # print("\n".join("".join("X" if cell > 0 else "#" if cell < 0 else " " for cell in row) for row in grid))

    print(f"Part 1: number of cells visited {num_visited}")


if __name__ == "__main__":
    covered_area()
