import operator
from functools import reduce


def load_input():
    with open("input", "r") as f:
        return [tuple(int(i) for i in l.split(",")) for l in f]


def main():
    boxes = load_input()
    squared_distances: list[tuple[int, int, int]] = []
    for i in range(len(boxes) - 1):
        xi, yi, zi = boxes[i]
        for j in range(i+1, len(boxes)):
            xj, yj, zj = boxes[j]
            d_ij = (xj-xi)**2 + (yj-yi)**2 + (zj-zi)**2
            squared_distances.append((i, j, d_ij))

    squared_distances.sort(key=operator.itemgetter(2))

    # Initially each box is its own singleton circuit
    circuits: list[set[int]] = [{i} for i in range(len(boxes))]
    unique_circuits: dict[int, set[int]] = {id(c): c for c in circuits}
    # iterate over the first thousand closest connections and merge the
    # circuits on each side of the connection - when two indices i and j
    # are part of the same circuit, then circuits[i] and circuits[j]
    # are *the same set object* (not just sets with the same members)
    for n, (i, j, d_ij) in enumerate(squared_distances):
        if n == 1000:
            break
        c_i = circuits[i]
        c_j = circuits[j]
        # First check if i and j are already in the same circuit - they might
        # be if this link creates a loop in an already-existing circuit
        if c_i is not c_j:
            # this link joins two circuits - add the elements of circuit i
            # to circuit j's set
            c_j.update(c_i)
            # drop the old i circuit
            del unique_circuits[id(c_i)]
            # and update the old references to circuit i's set to make them
            # point at the merged set instead
            for member_i in c_i:
                circuits[member_i] = c_j

    # sort unique circuits by size
    unique = list(unique_circuits.values())
    unique.sort(key=len, reverse=True)

    print(f"Product of 3 largest: {reduce(operator.mul, (len(c) for c in unique[:3]), 1)}")


if __name__ == "__main__":
    main()