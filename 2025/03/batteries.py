def read_input():
    with open("input", "r") as f:
        return [[int(v) for v in line.strip()] for line in f]


def part1():
    banks = read_input()
    total = 0
    for b in banks:
        hi_pos = len(b) - 2
        lo_pos = len(b) - 1
        for pos in range(hi_pos-1, -1, -1):
            if b[pos] >= b[hi_pos]:
                old_hi_pos, hi_pos = hi_pos, pos
                if b[old_hi_pos] > b[lo_pos]:
                    lo_pos = old_hi_pos

        total += 10*b[hi_pos] + b[lo_pos]

    print(f"Total maximum jolts: {total}")


if __name__ == "__main__":
    part1()