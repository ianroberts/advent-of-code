import json


def load_data():
    pairs = []
    with open("input", "r") as f:
        while True:
            p1 = json.loads(f.readline())
            p2 = json.loads(f.readline())
            pairs.append((p1, p2))

            if not f.readline():
                break

    return pairs


def lte(p1, p2):
    if isinstance(p1, int) and isinstance(p2, int):
        return None if p1 == p2 else p1 < p2

    list1 = p1 if isinstance(p1, list) else [p1]
    list2 = p2 if isinstance(p2, list) else [p2]
    for i1, i2 in zip(list1, list2):
        cmp = lte(i1, i2)
        if cmp is not None:
            return cmp

    lendiff = len(list1) - len(list2)
    if lendiff == 0:
        return None
    else:
        return lendiff < 0


def part1():
    pairs = load_data()

    result = 0
    for i, (p1, p2) in enumerate(pairs):
        if lte(p1, p2) is not False:
            result += i+1

    print(f"Sum of indices of correctly-ordered pairs: {result}")


def part2():
    pairs = load_data()
    div1 = [[2]]
    div2 = [[6]]
    lte_div1 = 0
    lte_div2 = 0

    for pair in pairs:
        for packet in pair:
            if lte(packet, div1) is not False:
                lte_div1 += 1
            if lte(packet, div2) is not False:
                lte_div2 += 1

    # Index of div1 is the number of packets that are lte [[2]], plus one (because
    # one-based indexing)
    # Index of div2 is the number of packets that are lte [[6]], plus one (because
    # one-based index), plus another one for the div1 packet
    print(f"Decoder key: {(lte_div1 + 1) * (lte_div2 + 2)}")


if __name__ == "__main__":
    part1()
    part2()
