def load_data():
    with open("input", "r") as f:
        return [int(line) for line in f]


def prng(n: int) -> int:
    n1 = n << 6
    n = (n ^ n1) & 0xFFFFFF
    n2 = n >> 5
    n = (n ^ n2) & 0xFFFFFF
    n3 = n << 11
    n = (n ^ n3) & 0xFFFFFF

    return n


def part1():
    seeds = load_data()

    total = 0
    for seed in seeds:
        for n in range(2000):
            seed = prng(seed)
        total += seed

    print(f"Total of 2000th numbers: {total}")


if __name__ == "__main__":
    part1()
