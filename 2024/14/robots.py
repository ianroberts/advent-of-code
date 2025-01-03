import re
from functools import reduce
from operator import mul
from aoc_common.grid import Cell

def load_data():
    digits = re.compile(r"-?\d+")
    with open("input", "r") as f:
        robots = []
        for line in f:
            line = line.strip()
            px, py, vx, vy = (int(m.group()) for m in digits.finditer(line))
            robots.append([Cell(py, px), Cell(vy, vx)])
    return robots


def one_hundred_steps():
    robots = load_data()

    quadrants = [0, 0, 0, 0]
    for p, v in robots:
        new_x = (p.col + (100*v.col)) % 101
        new_y = (p.row + (100*v.row)) % 103
        if new_x == 50 or new_y == 51:
            continue
        quadrants[int(new_x > 50) + 2*int(new_y > 51)] +=1

    print(f"safety: {reduce(mul, quadrants, 1)}")


def matrix(occupied: set[Cell], rows: range, cols: range) -> str:
    return "\n".join("".join("#" if Cell(r, c) in occupied else "." for c in cols) for r in rows)


def easter_egg():
    # It's not an Easter egg, it's a Christmas tree...
    robots = load_data()
    rows = range(103)
    cols = range(101)
    moves = 0

    mat = matrix(set(r[0] for r in robots), rows, cols)
    print(mat)

    while True:
        mat = matrix(set(r[0] for r in robots), rows, cols)
        if "#############" in mat:
            # Having that many robots in adjacent spaces is probably not a co-incidence
            print(f"-------------- {moves} moves ---------------")
            print(mat)
            if input("Keep going? ") == "n":
                break

        # make one move
        moves += 1
        for r in robots:
            p, v = r
            r[0] = Cell((p.row + v.row) % 103, (p.col + v.col) % 101)

        if (moves % 100) == 0:
            print(moves)



if __name__ == "__main__":
    one_hundred_steps()
    easter_egg()