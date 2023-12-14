from bitarray import bitarray


def input_patterns():
    cur_pattern = []
    with open("input", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                cur_pattern.append(bitarray(1 if c == '#' else 0 for c in line))
            else:
                if cur_pattern:
                    yield cur_pattern
                cur_pattern = []

    # yield the last pattern, if any
    if cur_pattern:
        yield cur_pattern


# Original list-based implementation of part 1
def find_mirror(pattern):
    l = len(pattern)
    for n in range(1, l):
        # how many steps can we go either forward or back from here before we fall off the end?
        run_max = min(n, l-n)
        # compare the run of that length up to here with the reverse of the run of the same
        # length after here
        if pattern[n-run_max:n] == pattern[n+run_max-1:n-1:-1]:
            return n

    return 0


def total_reflection():
    total = 0
    for i, pattern in enumerate(input_patterns()):
        h_mirror = find_mirror(pattern)
        total += 100 * h_mirror
        transpose = [bitarray(c) for c in zip(*pattern)]
        v_mirror = find_mirror(transpose)
        total += v_mirror
        print(f"Pattern {i} ({len(pattern)}x{len(pattern[0])}) mirrored at column {v_mirror}, row {h_mirror}")

    return total


# More general implementation to find a line that would be a mirror if exactly N points were flipped
def find_smudged_mirror(pattern, smudges):
    l = len(pattern)
    for n in range(1, l):
        run_max = min(n, l-n)
        diffs = 0
        for m in range(1, run_max+1):
            # Number of differences between the rows m either side of a mirror at n is equal
            # to the number of one-bits in the bitwise xor of the two lines
            diffs += (pattern[n-m] ^ pattern[n+m-1]).count()
            if diffs > smudges:
                # this can't be a smudged mirror line
                break

        else:
            if diffs == smudges:
                # this can be a smudged mirror line
                return n

    return 0


def total_reflections_with_smudges(smudges):
    total = 0
    for i, pattern in enumerate(input_patterns()):
        h_mirror = find_smudged_mirror(pattern, smudges)
        total += 100 * h_mirror
        transpose = [bitarray(c) for c in zip(*pattern)]
        v_mirror = find_smudged_mirror(transpose, smudges)
        total += v_mirror

    return total



if __name__ == "__main__":
    print(f"Reflection summary {total_reflection()}")
    print(f"With one smudge: {total_reflections_with_smudges(1)}")
    print(f"With no smudges, using general algorithm: {total_reflections_with_smudges(0)}")

