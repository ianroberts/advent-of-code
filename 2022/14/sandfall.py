from itertools import pairwise

from aoc_common.grid import Cell, Direction


def load_data():
    blocked: set[Cell] = set()
    with open("input", "r") as f:
        for path in f:
            path = path.strip()
            corners = []
            for corner in path.split(" -> "):
                c, r = corner.split(",")
                corners.append(Cell(int(r), int(c)))
            for a, b in pairwise(corners):
                a_to_b = b - a
                if a_to_b.col == 0:
                    vec = a_to_b // (abs(a_to_b.row))
                else:
                    vec = a_to_b // abs(a_to_b.col)

                blocked.add(a)
                while a != b:
                    a += vec
                    blocked.add(a)

    return blocked


def part1():
    blocked = load_data()
    walls = blocked.copy()
    bottom_row = max(r for (r, c) in blocked)

    units_of_sand = 0
    done = False
    while not done:
        pos = Cell(0, 500)
        while True:
            if pos.row >= bottom_row:
                # sand is trickling into the void
                done = True
                break
            if ((candidate := pos + Direction.SOUTH) not in blocked) or ((candidate := pos + Direction.SW) not in blocked) or ((candidate := pos + Direction.SE) not in blocked):
                # this unit of sand can move somewhere - move it
                pos = candidate
            else:
                # this unit of sand cannot move, it has come to rest
                blocked.add(pos)
                units_of_sand += 1
                break

    min_col = min(c for r, c in blocked)
    max_col = max(c for r, c in blocked)

    for r in range(bottom_row + 2):
        print("".join("#" if Cell(r, c) in walls else "o" if Cell(r, c) in blocked else "." for c in range(min_col-2, max_col+3)))


    print(f"Units of sand that can come to rest: {units_of_sand}")


def part2():
    blocked = load_data()
    walls = blocked.copy()
    floor = max(r for (r, c) in blocked) + 2

    def is_free(c: Cell):
        return c.row != floor and c not in blocked

    units_of_sand = 0
    while True:
        pos = Cell(0, 500)
        if pos in blocked:
            break

        while True:
            if (is_free(candidate := pos + Direction.SOUTH)) or (is_free(candidate := pos + Direction.SW)) or (is_free(candidate := pos + Direction.SE)):
                # this unit of sand can move somewhere - move it
                pos = candidate
            else:
                # this unit of sand cannot move, it has come to rest
                blocked.add(pos)
                units_of_sand += 1
                break

    min_col = min(c for r, c in blocked)
    max_col = max(c for r, c in blocked)

    for r in range(floor + 1):
        print("".join("#" if (r == floor or Cell(r, c) in walls) else "o" if Cell(r, c) in blocked else "." for c in range(min_col-2, max_col+3)))

    print(f"Units of sand that can come to rest (part 2): {units_of_sand}")



if __name__ == "__main__":
    part1()
    part2()
