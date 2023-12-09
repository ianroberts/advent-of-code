from itertools import repeat, cycle, count


def register_values():
    x = 1
    yield x  # x during the first cycle, before any instructions have been run
    with open("input", "r") as f:
        for line in f:
            line = line.strip()
            if line == "noop":
                yield x
            else:  # it's an addx
                add = int(line[5:])
                # addx takes two cycles, x has the old value after cycle 1
                yield x
                # and the new value after cycle 2
                x += add
                yield x

    # No more instructions, so keep yielding the same x for ever
    yield from repeat(x)


def signal_strength():
    interesting_strength = 0
    # Signal strength is cycle number * register value _during_ that cycle.
    for cycle_number, x in zip(count(1), register_values()):
        print(f"{cycle_number=}, {x=}")
        if cycle_number > 240:
            break

        if cycle_number == 20 or (cycle_number-20) % 40 == 0:
            interesting_strength += x * cycle_number

    return interesting_strength


def pretty_picture():
    for cycle_number, col, x in zip(count(1), cycle(range(40)), register_values()):
        if cycle_number > 240:
            break

        if col == 0:
            # move to next line
            print("")
        if abs(x-col) <= 1:
            print("█", end="")
        else:
            print(".", end="")


if __name__ == "__main__":
    print(f"Sum of interesting strengths: {signal_strength()}")
    pretty_picture()
