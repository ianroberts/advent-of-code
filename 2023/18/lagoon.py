# Naïve algorithm for part 1

from collections import namedtuple
Cell = namedtuple("Cell", ["row", "col"])


def dig_trench():
    turtle = Cell(0, 0)
    trench = {turtle: []}
    with open("input", "r") as f:
        for line in f:
            direction, dist, rgb = line.strip().split(' ', 2)
            if direction == "U":
                step = Cell(-1, 0)
            elif direction == "D":
                step = Cell(1, 0)
            elif direction == "L":
                step = Cell(0, -1)
            elif direction == "R":
                step = Cell(0, 1)
            reverse_step = Cell(-step.row, -step.col)

            for n in range(int(dist)):
                # Record that the previous visited cell has a link of the step we just made
                trench[turtle].append(step)
                turtle = Cell(turtle.row + step.row, turtle.col + step.col)
                # Record that this new cell has a link back to the one we last visited
                this_cell = trench.setdefault(turtle, [])
                this_cell.append(reverse_step)

    return trench


def lagoon_size():
    trench = dig_trench()
    min_col = min(c.col for c in trench)
    max_col = max(c.col for c in trench)
    min_row = min(c.row for c in trench)
    max_row = max(c.row for c in trench)

    total_area = 0
    for row in range(min_row, max_row+1):
        inside = False
        for col in range(min_col, max_col+1):
            this_cell = trench.get(Cell(row, col))
            if this_cell or inside:
                total_area += 1
            if this_cell and Cell(1, 0) in this_cell:
                inside = not inside

    return total_area


if __name__ == "__main__":
    print(f"Total lagoon size: {lagoon_size()}")
