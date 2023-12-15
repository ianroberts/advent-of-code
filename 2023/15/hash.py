import re
from functools import reduce


def parse_input():
    with open("input", "r") as f:
        return "".join(line.strip() for line in f).split(",")


def hash_of(seq):
    return reduce(lambda val, char: ((val + ord(char)) * 17) % 256, seq, 0)


def calculate_hash():
    steps = parse_input()
    return sum(hash_of(step) for step in steps)


step_re = re.compile(r"^([a-z]+)([=-])(\d?)$")


def lens_power():
    steps = parse_input()
    # list of boxes, where each box is a list of (label, focal_length) tuples
    boxes: list[list[tuple[str, int]]] = [[] for _ in range(256)]
    for step in steps:
        label, op, val = step_re.search(step).groups()
        box = boxes[hash_of(label)]
        # Find the index of the lens with this label in the box, if present, or None if not
        label_idx = next((i for i, (lbl, _) in enumerate(box) if lbl == label), None)
        if op == "-":
            # Remove the lens with this label from the box - the following lenses will
            # "shift forwards" automatically
            if label_idx is not None:
                box.pop(label_idx)
        else:  # op == "="
            if label_idx is None:
                # this label is not currently in the box - add at the back
                box.append((label, val))
            else:
                # this label _is_ in the box, swap it out in-place
                box[label_idx] = (label, val)

    # summarise the total power
    return sum((i + 1) * (j + 1) * int(fl) for i, box in enumerate(boxes) for j, (_, fl) in enumerate(box))


if __name__ == "__main__":
    print(f"Part 1: sum of instruction hashes = {calculate_hash()}")
    print(f"Total lens power: {lens_power()}")
