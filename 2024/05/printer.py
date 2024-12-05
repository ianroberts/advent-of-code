from itertools import combinations


def load_data():
    with open("input", "r") as f:
        rules = set()
        for line in f:
            line = line.strip()
            if line == "":
                break
            rules.add(tuple(line.split("|")))

        orderings = []
        for line in f:
            line = line.strip()
            orderings.append(line.split(","))

    return rules, orderings


def is_valid(rules, ordering):
    for i in range(1, len(ordering)):
        if any((ordering[i], x) in rules for x in ordering[:i]):
            return False

    return True


def valid_orderings():
    rules, orderings = load_data()
    total_middles = 0
    for ordering in orderings:
        if is_valid(rules, ordering):
            total_middles += int(ordering[len(ordering) // 2])

    print(f"Total of middle values: {total_middles}")


def fix_invalid():
    rules, orderings = load_data()
    total_middles = 0
    for ordering in orderings:
        if not is_valid(rules, ordering):
            # Naive bubble sort is fast enough for this data set
            for j in range(len(ordering) - 1, 0, -1):
                for i in range(j, len(ordering)):
                    if (ordering[i], ordering[i - 1]) in rules:
                        ordering[i - 1], ordering[i] = ordering[i], ordering[i - 1]

            total_middles += int(ordering[len(ordering) // 2])

    print(f"Total middle values of invalid-but-fixed orderings: {total_middles}")


def are_rules_total():
    """
    Check my hunch on the form of the input data - the question doesn't say this
    explicitly, but looking at the data file it looked like, for each set of pages,
    the rules specified one order or other (but never both) for every possible
    pair of numbers in that set - the rule set isn't necessarily a total
    ordering over arbitrary data, but it _is_ a total ordering over each of the
    page number sets in my specific input.

    Given this fact, I don't have to do anything particularly clever to answer part
    2, any naive sorting algorithm (using the rules as its comparator function) will work.
    """
    rules, orderings = load_data()
    print(
        all(((i, j) in rules) != ((j, i) in rules) for ordering in orderings for (i, j) in combinations(ordering, 2))
    )


if __name__ == "__main__":
    are_rules_total()
    valid_orderings()
    fix_invalid()
