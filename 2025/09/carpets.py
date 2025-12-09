from aoc_common.grid import Cell


def load_input():
    with open("input", "r") as f:
        return [Cell(int(r), int(c)) for r, c in (l.split(",") for l in f)]


def sign(x):
    return 0 if x == 0 else 1 if x > 0 else -1


def boundary(corners):
    edges = {corners[0]: []}
    for i in range(len(corners)):
        corner_a = corners[i]
        corner_b = corners[(i + 1) % len(corners)]
        step = Cell(sign(corner_b.row - corner_a.row), sign(corner_b.col - corner_a.col))
        # link first corner to second with the forward step
        edges.setdefault(corner_a, []).append(step)
        # link second corner back to first with the reverse step
        edges.setdefault(corner_b, []).append(-step)

    # At this point edges has entries for all the corners where we change direction.
    # Next we want to subdivide the grid into larger rectangles, essentially collapsing
    # down any range of columns that only contains horizontal edges, and any range of
    # rows that only contains vertical edges, into a "virtual column" or "virtual row"
    # of the appropriate length
    corner_columns = sorted(set(cell.col for cell in edges))
    corner_rows = sorted(set(cell.row for cell in edges))

    last_corner = corner_rows[0]
    row_heights = [1]
    rows_map = {last_corner: 0}
    for i in range(1, len(corner_rows)):
        row_heights.append(corner_rows[i] - last_corner - 1)  # The "gap" between the last row and this
        row_heights.append(1)  # The height of the corner row
        last_corner = corner_rows[i]
        rows_map[last_corner] = 2 * i

    last_corner = corner_columns[0]
    column_widths = [1]
    columns_map = {last_corner: 0}
    for i in range(1, len(corner_columns)):
        column_widths.append(corner_columns[i] - last_corner - 1)  # The "gap" between the last col and this
        column_widths.append(1)  # The width of the corner col
        last_corner = corner_columns[i]
        columns_map[last_corner] = 2 * i

    scaled_corners = [Cell(rows_map[c.row], columns_map[c.col]) for c in corners]
    bounds = {}
    for i in range(len(corners)):
        corner_a = corners[i]
        corner_b = corners[(i + 1) % len(corners)]
        new_corner_a = scaled_corners[i]
        new_corner_b = scaled_corners[(i + 1) % len(scaled_corners)]
        bounds[new_corner_a] = edges[corner_a]
        bounds[new_corner_b] = edges[corner_b]
        if corner_b.row - corner_a.row == 0:
            # horizontal edge
            for c in range(min(new_corner_a.col, new_corner_b.col) + 1, max(new_corner_a.col, new_corner_b.col)):
                edge_cell = Cell(new_corner_a.row, c)
                bounds[edge_cell] = [Cell(0, -1), Cell(0, 1)]
        else:
            # vertical edge
            for r in range(min(new_corner_a.row, new_corner_b.row) + 1, max(new_corner_a.row, new_corner_b.row)):
                edge_cell = Cell(r, new_corner_a.col)
                bounds[edge_cell] = [Cell(-1, 0), Cell(1, 0)]

    return scaled_corners, bounds, row_heights, column_widths


def part2(red):
    scaled_corners, bounds, row_heights, column_widths = boundary(red)

    # compute inside or outside for each point in the grid
    is_inside = []
    for row in range(len(row_heights) + 1):
        isin = []
        is_inside.append(isin)
        inside = False
        for col in range(len(column_widths) + 1):
            this_cell = bounds.get(Cell(row, col))
            isin.append(bool(this_cell or inside))
            if this_cell and Cell(1, 0) in this_cell:
                inside = not inside

    # Now we can find the biggest rect such that all its points are inside the bounds
    biggest_rect = 0
    for i in range(len(red) - 1):
        for j in range(i + 1, len(red)):
            ci = red[i]
            sci = scaled_corners[i]
            cj = red[j]
            scj = scaled_corners[j]

            topleft = Cell(min(sci.row, scj.row), min(sci.col, scj.col))
            bottomright = Cell(max(sci.row, scj.row), max(sci.col, scj.col))
            if any((not is_inside[r][c]) for r in range(topleft.row, bottomright.row+1) for c in range(topleft.col, bottomright.col+1)):
                # This rect is not inside the bounds
                continue

            # each side length of the rectangle is the difference in that
            # coordinate, plus one to include the edge row/col
            area = (abs(ci.row - cj.row) + 1) * (abs(ci.col - cj.col) + 1)
            if area > biggest_rect:
                biggest_rect = area

    print(f"{biggest_rect=}")


def part1(red):

    biggest_rect = 0
    for i in range(len(red) - 1):
        for j in range(i + 1, len(red)):
            ci = red[i]
            cj = red[j]
            # each side length of the rectangle is the difference in that
            # coordinate, plus one to include the edge row/col
            area = (abs(ci.row - cj.row) + 1) * (abs(ci.col - cj.col) + 1)
            if area > biggest_rect:
                biggest_rect = area

    print(f"{biggest_rect=}")


if __name__ == "__main__":
    red_tiles = load_input()
    part1(red_tiles)
    part2(red_tiles)
