

def parse_input():
    with open("input", "r") as f:
        for line in f:
            line = line.strip()
            e1, e2 = line.split(",")
            e11, e12 = (int(n) for n in e1.split("-"))
            e21, e22 = (int(n) for n in e2.split("-"))
            yield (range(e11, e12+1), range(e21, e22+1))


def fully_contained():
    contained = 0
    for range1, range2 in parse_input():
        if (range1.start in range2 and range1[-1] in range2) or (range2.start in range1 and range2[-1] in range1):
            contained += 1

    return contained


def overlapping():
    overlap = 0
    for range1, range2 in parse_input():
        if range1.start > range2.start:
            range1, range2 = range2, range1
        if range1.stop > range2.start:
            overlap += 1

    return overlap


if __name__ == "__main__":
    print(f"fully contained pairs: {fully_contained()}")
    print(f"overlapping pairs: {overlapping()}")
