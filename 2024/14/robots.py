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
            robots.append((Cell(py, px), Cell(vy, vx)))
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


if __name__ == "__main__":
    one_hundred_steps()