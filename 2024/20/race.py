from aoc_common.grid import Cell


def load_data():
    with open("input", "r") as f:
        grid = [l.strip() for l in f]

    start = end = None
    # Find the start and end, changing their character in the grid to "."
    # to simplify the later comparisons
    for r in range(len(grid)):
        l = grid[r]
        if (start_col := l.find("S")) >= 0:
            start = Cell(r, start_col)
            grid[r] = l = l.replace("S", ".")

        if (end_col := l.find("E")) >= 0:
            end = Cell(r, end_col)
            grid[r] = l = l.replace("E", ".")

    if not start or not end:
        raise ValueError("Invalid track")

    # We know there is exactly one route from start to end, trace along
    # the route storing the distance-from-start for every "." cell we hit.
    track: dict[Cell, int] = {start: 0}
    cur = start
    prev = None
    distance = 0
    while cur != end:
        distance += 1
        prev, cur = cur, next(
            n for n in cur.neighbours() if n.of(grid) == "." and n != prev
        )
        track[cur] = distance

    return grid, track, start, end


def cheats_up_to(distance: int, saving: int):
    grid, track, start, end = load_data()
    valid_rows = range(len(grid))
    valid_cols = range(len(grid[0]))

    cheats = [0 for _ in range(len(track))]
    for origin, origin_dist in track.items():
        # Look at all cells within Manhattan metric "distance" of origin that are
        # (a) on the track but (b) further away via the track than they would be
        # via the cheat route
        for r in range(-distance, distance + 1):
            if origin.row + r not in valid_rows:
                continue
            for c in range(abs(r) - distance, -abs(r) + distance + 1):
                if origin.col + c not in valid_cols:
                    continue
                cell = origin + Cell(r, c)
                # Manhattan distance from origin to this cell
                d_from_o = abs(r) + abs(c)
                if (
                    cell.of(grid) == "."
                    and track.get(cell, -1) > origin_dist + d_from_o
                ):
                    # This is a shortcut whose saving is the difference between the
                    # distance from origin to endpoint via the racetrack and via the
                    # cheat path
                    cheats[track[cell] - origin_dist - d_from_o] += 1

    print(f"Shortcuts saving >={saving}: {sum(cheats[saving:])}")


if __name__ == "__main__":
    # Part 1
    cheats_up_to(2, 100)
    # Part 2
    cheats_up_to(20, 100)
