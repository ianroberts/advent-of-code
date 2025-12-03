import functools


def read_input():
    with open("input", "r") as f:
        return [[int(v) for v in line.strip()] for line in f]


def total_jolts(n):
    """
    Find the maximum total joltage from n batteries in each bank.
    """
    banks = read_input()
    total = 0
    for b in banks:
        # Start with the base case - the last n battery positions
        positions = list(range(len(b)-n, len(b)))
        # Now work towards the front of the bank, each time work out whether
        # the battery at this position is "at least as good" as the first
        # (i.e. most significant) battery in the current best subsequence.
        # If it is, then we essentially need to swap this battery for one of
        # the later (less significant) ones in the subsequence.
        #
        # Any new batteries we swap in as this search progresses will always
        # have at least as high a value as their successor in the subsequence,
        # so the one we want to take out will always be the last one in the
        # subsequence *except* where the tail of the subsequence is still some
        # of the initial "last n" - in this situation some of the batteries in
        # this tail may still be "smaller" than their immediate successor,
        # and the first such battery will be the one to eject.
        for pos in range(positions[0]-1, -1, -1):
            if b[pos] >= b[positions[0]]:
                # we can produce a higher number by using this pos instead
                # of the previous highest
                positions.insert(0, pos)
                # see if there's still a "tail" battery that is smaller
                # than its current successor, eject the first such if it
                # exists...
                for j in range(1, len(positions)-1):
                    if b[positions[j]] < b[positions[j+1]]:
                        positions.pop(j)
                        break
                # ... or the last battery in the whole subsequence if not
                if len(positions) > n:
                    positions.pop()

        # The "total joltage" of this subsequence is what you get by treating
        # the battery values at each position as a base-10 integer, i.e.
        # iterate through the positions each time shifting the previous
        # result one place to the left (*10) then adding the value at the
        # current position
        total += functools.reduce(lambda acc, p: 10*acc + b[p], positions, 0)

    print(f"Total maximum jolts for {n=}: {total}")


if __name__ == "__main__":
    # part 1
    total_jolts(2)
    # part 2
    total_jolts(12)