import re
from functools import cache


def load_data():
    with open("input", "r") as f:
        towels = f.readline().strip().split(", ")

        # Skip blank
        f.readline()

        patterns = [l.strip() for l in f]

    return towels, patterns


def part1():
    towels, patterns = load_data()
    # Let the built-in regex engine do the heavy lifting of building and
    # searching the automaton for me... I'll probably have to do this myself
    # for part 2
    towelpattern = re.compile("(?:" + "|".join(towels) + ")+")
    valid = []
    for pat in patterns:
        if towelpattern.fullmatch(pat):
            valid.append(pat)

    print(f"Number of possible patterns: {len(valid)}")
    return towels, valid


def part2(towels, patterns):
    """
    Given a set of towels and a set of patterns that we know are possible (from part 1),
    count how many ways each pattern can be formed from the given towels.
    """

    # hello functools my old friend...
    @cache
    def num_matches(pattern):
        # Termination condition - if we've stripped off prefixes for the entire
        # pattern then by the time we reach here we have found _one_ way to match
        if pattern == "":
            return 1

        # Otherwise, add up the total matches that we would get for the shorter
        # pattern obtained by stripping off each possible towel prefix
        total = 0
        for t in towels:
            if pattern.startswith(t):
                total += num_matches(pattern[len(t) :])

        return total

    print(f"Total ways to match: {sum(num_matches(p) for p in patterns)}")


if __name__ == "__main__":
    towels, valid = part1()
    part2(towels, valid)
