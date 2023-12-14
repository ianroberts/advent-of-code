
def parse_input():
    with open("input", "r") as f:
        # Add a blocker to the end of each row as it avoids the edge effect for part 2
        return [[c for c in line.strip() + "#"] for line in f]


# part 1
def total_load():
    matrix = parse_input()
    rows = len(matrix)
    load = 0
    # Keep track for each column index of the number of spaces (.) above that column of the
    # current row until the next # or the top edge.  This is the number of places each O in
    # the current row would be displaced north if the platform were tilted that way.
    spaces_above = [0 for _ in range(len(matrix[0]))]
    for i, row in enumerate(matrix):
        for j, c in enumerate(row):
            if c == ".":
                spaces_above[j] += 1
            elif c == "#":
                spaces_above[j] = 0
            else:  # c == "O"
                # Added load for this rock is the load if it were in the current row i, plus
                # one for each space it can roll north
                load += rows - i + spaces_above[j]

    return load


def elt_from_north(m, r, c, value=None):
    """Return or set an element in m in normal orientation (with origin at the north west)
    with rows top to bottom and columns from left to right"""
    if value is None:
        return m[r][c]
    else:
        m[r][c] = value


def elt_from_west(m, r, c, value=None):
    """Return or set an element in m rotated 90 degrees right, so "rows" are the columns
    of the real matrix from left to right and "columns" are the rows from bottom to top
    (origin is the south west corner)"""
    if value is None:
        return m[-c-1][r]
    else:
        m[-c-1][r] = value


def elt_from_south(m, r, c, value=None):
    """Return or set an element in m rotated 180 degrees, so rows are rows but count from
    bottom to top and columns are columns but count from right to left (origin is in the
    south east corner)"""
    if value is None:
        return m[-r-1][-c-1]
    else:
        m[-r-1][-c-1] = value


def elt_from_east(m, r, c, value=None):
    """Return or set an element in m rotated 90 degrees left, so "rows" are the original columns
    from right to left and "columns" are the original rows from top to bottom (origin is the
    north east corner)"""
    if value is None:
        return m[c][-r-1]
    else:
        m[c][-r-1] = value


def tilt(matrix, elt, rows, columns):
    # Keep track for each column index of the number of spaces (.) above that column of the
    # current row until the next # or the top edge.  This is the number of places each O in
    # the current row must be displaced north to tilt the platform that way.
    spaces_above = [0 for _ in range(len(matrix[0]))]
    for i in range(rows):
        for j in range(columns):
            c = elt(matrix, i, j)
            if c == ".":
                spaces_above[j] += 1
            elif c == "#":
                spaces_above[j] = 0
            else:  # c == "O"
                # Move this rock as far as it can go
                tmp = elt(matrix, i - spaces_above[j], j)
                elt(matrix, i - spaces_above[j], j, c)
                elt(matrix, i, j, tmp)


def spin(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    tilt(matrix, elt_from_north, rows, cols)
    tilt(matrix, elt_from_west, cols, rows)
    tilt(matrix, elt_from_south, rows, cols)
    tilt(matrix, elt_from_east, cols, rows)

    rocks = 0
    signature = []
    for row in matrix:
        row_sig = []
        signature.append(row_sig)
        for c in row:
            if c == "O":
                rocks += 1
            elif c == "#":
                row_sig.append(rocks)
                rocks = 0

    return tuple(tuple(row) for row in signature)


def total_load_after(spins):
    matrix = parse_input()
    spin_sigs = {}
    i = 0
    cycle_start = None
    cycle_length = 0
    while True:
        i += 1
        sig = spin(matrix)
        if sig in spin_sigs:
            # we have found the cycle
            cycle_start = spin_sigs[sig]
            cycle_length = i - cycle_start
            print(f"State {cycle_start} repeats at {i} - cycle length {cycle_length}")
            break

        spin_sigs[sig] = i

    # the matrix is now at the beginning of a cycle, how much further do we need to go?
    # subtract the cycle start
    spins_after_cycle_start = spins - cycle_start
    # and take the remainder modulo cycle_length
    overflow_spins = spins_after_cycle_start % cycle_length
    print(f"{spins} spins made up of {cycle_start} initial spins plus "
          f"{spins_after_cycle_start // cycle_length} complete cycles of {cycle_length} plus "
          f"{overflow_spins} additional spins")

    # Do that many more cycles
    for _ in range(overflow_spins):
        sig = spin(matrix)

    # and calculate the load from the final signature, where each row conveniently sums to the number of
    # O elements in that row of the matrix
    return sum((len(matrix)-i) * sum(r) for i, r in enumerate(sig))


if __name__ == "__main__":
    print(f"Total load tilted north: {total_load()}")
    print(f"Total load after 1,000,000,000 cycles: {total_load_after(1_000_000_000)}")
