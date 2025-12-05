from black import ranges


def load_input():
    with open("input", "r") as f:
        ranges = []
        for line in f:
            line = line.strip()
            if line == "":
                break
            start, end = line.split("-")
            ranges.append(range(int(start), int(end) + 1))  # +1 to make the end inclusive

        # remaining lines are the available IDs
        available = [int(l) for l in f]

    # amalgamate overlapping and adjacent ranges (this is not
    # necessary for part 1, but it is for part 2):
    ranges.sort(key=lambda r: r.start)
    i = 0
    while i < len(ranges) - 1:
        r_i, r_j = ranges[i], ranges[i + 1]
        if r_i.stop < r_j.start:
            # there's at least 1 number not included in either range
            i += 1
        else:
            # this range overlaps or butts right up to the next one;
            # replace both ranges with a single range spanning the
            # whole interval
            ranges[i : i + 2] = [range(r_i.start, max(r_i.stop, r_j.stop))]

    return ranges, available


def main():
    ranges, ids = load_input()
    print("Part 1: number of available ingredients that are fresh")
    print(sum(1 for i in ids if any(i in r for r in ranges)))
    print("Part 2: number of possible IDs that are fresh")
    print(sum(len(r) for r in ranges))


if __name__ == "__main__":
    main()
