from functools import cache
from math import floor, log10


def load_data():
    with open("input", "r") as f:
        data = f.read().strip()
        return [int(n) for n in data.split()]


@cache
def num_stones(start: int, iterations: int) -> int:
    if iterations == 0:
        return 1

    if start == 0:
        return num_stones(1, iterations - 1)
    if (log := floor(log10(start))) % 2 == 1:
        divide = 10 ** ((log // 2) + 1)
        return sum(num_stones(x, iterations - 1) for x in divmod(start, divide))

    return num_stones(start * 2024, iterations - 1)


def main():
    data = load_data()

    print(f"Part 1: {sum(num_stones(d, 25) for d in data)}")
    print(f"Part 2: {sum(num_stones(d, 75) for d in data)}")


if __name__ == "__main__":
    main()
