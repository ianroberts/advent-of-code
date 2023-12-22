from collections import namedtuple
Cell = namedtuple("Cell", ["row", "col"])


def dig_trench():
    turtle = Cell(0, 0)
    corners = []
    trench_edges = {turtle: []}
    with open("input", "r") as f:
        for line in f:
            _, _, rgb = line.strip().split(' ', 2)
            # decode the hex code
            direction = rgb[-2]  # last digit before the close parenthesis
            dist = int(rgb[2:-2], 16)
            print(f"{direction=}, {dist=}")
            if direction == "3":
                step = Cell(-1, 0)
            elif direction == "1":
                step = Cell(1, 0)
            elif direction == "2":
                step = Cell(0, -1)
            elif direction == "0":
                step = Cell(0, 1)
            reverse_step = Cell(-step.row, -step.col)

            # Record that the previous visited cell has a link of the step we just made
            trench_edges[turtle].append(step)
            corners.append(turtle)
            turtle = Cell(turtle.row + step.row * dist, turtle.col + step.col * dist)
            # Record that this new cell has a link back to the one we last visited
            this_cell = trench_edges.setdefault(turtle, [])
            this_cell.append(reverse_step)

    # At this point trench has entries for all the corners where we change direction.
    # Next we want to subdivide the grid into larger rectangles, essentially collapsing
    # down any range of columns that only contains horizontal edges, and any range of
    # rows that only contains vertical edges, into a "virtual column" or "virtual row"
    # of the appropriate length
    corner_columns = sorted(set(cell.col for cell in trench_edges))
    corner_rows = sorted(set(cell.row for cell in trench_edges))

    last_corner = corner_rows[0]
    row_heights = [1]
    rows_map = {last_corner: 0}
    for i in range(1, len(corner_rows)):
        row_heights.append(corner_rows[i] - last_corner - 1)  # The "gap" between the last row and this
        row_heights.append(1)  # The height of the corner row
        last_corner = corner_rows[i]
        rows_map[last_corner] = 2*i

    last_corner = corner_columns[0]
    column_widths = [1]
    columns_map = {last_corner: 0}
    for i in range(1, len(corner_columns)):
        column_widths.append(corner_columns[i] - last_corner - 1)  # The "gap" between the last col and this
        column_widths.append(1)  # The width of the corner col
        last_corner = corner_columns[i]
        columns_map[last_corner] = 2*i

    trench = {}
    for i in range(len(corners)):
        corner_a = corners[i]
        corner_b = corners[(i+1) % len(corners)]
        new_corner_a = Cell(rows_map[corner_a.row], columns_map[corner_a.col])
        new_corner_b = Cell(rows_map[corner_b.row], columns_map[corner_b.col])
        trench[new_corner_a] = trench_edges[corner_a]
        trench[new_corner_b] = trench_edges[corner_b]
        if corner_b.row - corner_a.row == 0:
            # horizontal edge
            for c in range(min(new_corner_a.col, new_corner_b.col) + 1, max(new_corner_a.col, new_corner_b.col)):
                edge_cell = Cell(new_corner_a.row, c)
                trench[edge_cell] = [Cell(0, -1), Cell(0, 1)]
        else:
            # vertical edge
            for r in range(min(new_corner_a.row, new_corner_b.row) + 1, max(new_corner_a.row, new_corner_b.row)):
                edge_cell = Cell(r, new_corner_a.col)
                trench[edge_cell] = [Cell(-1, 0), Cell(1, 0)]

    return trench, row_heights, column_widths


def lagoon_size():
    trench, row_heights, column_widths = dig_trench()
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
                total_area += row_heights[row] * column_widths[col]
            if this_cell and Cell(1, 0) in this_cell:
                inside = not inside

    return total_area


if __name__ == "__main__":
    print(f"Total lagoon size (from hex): {lagoon_size()}")
