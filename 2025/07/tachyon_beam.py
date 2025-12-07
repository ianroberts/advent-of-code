def load_input():
    # We don't need to represent the whole grid, all we care about
    # is the column position of the beam source, and the set of
    # column positions for each row of splitters
    start_col: int = -1
    splitters: list[set[int]] = []
    with open("input", "r") as f:
        for line in f:
            if (s := line.find("S")) >= 0:
                start_col = s
            elif "^" in line:
                splitter_cols = set()
                c = -1
                while (c := line.find("^", c + 1)) >= 0:
                    splitter_cols.add(c)
                splitters.append(splitter_cols)

    return start_col, splitters


def main():
    start_col, splitters = load_input()
    # How many splitters have the beams encountered in total
    total_splits = 0
    # Which columns have a beam at this point in the descent
    beams: set[int] = {start_col}
    # How many different routes could a particle have taken to reach each
    # column position by the current level - there's far too many routes
    # to actually enumerate them all, but we only care about the *number*
    # of routes, not which routes they actually were.
    timelines: dict[int, int] = {start_col: 1}

    for row in splitters:
        for splitter in row:
            if splitter in beams:
                # part 1: count splits
                # this splitter will add one more split to the total ...
                total_splits += 1
                # ... extinguish the incoming beam ...
                beams.remove(splitter)
                # ... and add new beams to its left and right, if they
                # weren't already there
                beams.add(splitter - 1)
                beams.add(splitter + 1)

                # part 2: count timelines
                routes_to_here = timelines[splitter]  # definitely exists
                routes_to_left = timelines.get(splitter - 1, 0)  # assume 0 if not found
                routes_to_right = timelines.get(splitter + 1, 0)
                # this splitter will extinguish the beam at its own
                # position
                del timelines[splitter]
                # and all the possible routes to this splitter now
                # become possible routes to its left and right sides
                # (in addition to any existing routes if there's
                # already a beam at that column that originated from
                # a different splitter)
                timelines[splitter - 1] = routes_to_left + routes_to_here
                timelines[splitter + 1] = routes_to_right + routes_to_here

    print(f"{total_splits=}")
    print(f"Total timelines: {sum(timelines.values())}")


if __name__ == "__main__":
    main()
