import operator
from functools import reduce
from itertools import combinations
from typing import Iterable, Literal
from time import perf_counter

# Prime numbers under 50 - this will cover all cases for numbers with up
# to 100 digits...
small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]


def equal_magnitude_ranges(start, end) -> Iterable[tuple[str, str]]:
    """
    Split up a range of numbers (given as strings of digits) into
    sub-ranges such that both endpoints of every sub-range have
    the same number of digits.  If start and end already have the
    same length this is trivial, if end has more digits than start
    then, we split the range up into:

      - ``start`` -> 999...99 (same number of 9s as the length of
        ``start``)
      - 1000...0 -> 9999...9 for each length strictly between that
        of ``start`` and ``end`` (possibly none of them)
      - 1000...0 -> ``end`` (length of ``end``)
    """
    next_start = 10 ** (len(start))

    # (if len(start) == len(end) this will be an empty range, so
    # the for loop is a no-op)
    for l in range(len(start), len(end)):
        yield start, str(next_start - 1)
        start = str(next_start)
        next_start = next_start * 10
    yield start, end


def possible_splits(num_digits) -> Iterable[tuple[int, Literal[1, -1]]]:
    """
    Given a number of digits, determine the ways that a number
    with that many digits could be divided into equal-sized chunks,
    and yield a list of ``(chunk_length, sign)`` tuples defining which
    splits we need to check for duplicates.  The logic is as follows:

      1. Find all the distinct prime factors of ``num_digits``.
         Only *distinct* factors matter here, since any sequence
         of digits that is a pattern of ``M`` digits repeating
         ``N*p`` times will also be a pattern of ``M*N`` digits
         repeating ``p`` times for all values of ``N``, i.e. the
         set of repeating patterns for ``N*p`` chunks is a strict
         subset of the set of repeating patterns for ``p`` chunks.
      2. By the inclusion-exclusion principle, if we want to count
         all the possible repeating patterns without double-counting
         anything, then we need to add up the number of repeats in
         ``p`` chunks for each prime factor ``p`` (the single sets),
         then subtract the number of repeats in ``p*q`` chunks for
         all pairs of prime factors ``p`` and ``q`` (the
         2-intersections), then add back the number of repeats in
         ``p*q*r`` chunks for all triples (the 3-intersections),
         etc. etc. (where as always we only care about chunk counts
         that evenly divide the original length; any that don't will
         implicitly have no repeats).

    Therefore, what this generator yields is ``(num_digits // n, +1)``
    for each ``n`` that is a combination of an *odd* number of prime
    factors, and ``(num_digits // n, -1)`` for each ``n`` that is a
    combination of an *even* number of prime factors, as always only
    for ``n`` that evenly divides the original length.
    """
    prime_factors = [p for p in small_primes if num_digits % p == 0]
    for n in range(1, len(prime_factors) + 1):
        for group in combinations(prime_factors, n):
            num_chunks = reduce(operator.mul, group, 1)
            chunk_length, remainder = divmod(num_digits, num_chunks)
            if remainder == 0:
                yield chunk_length, 1 if len(group) % 2 == 1 else -1


def sum_repeats(l: str, r: str, length: int) -> int:
    """
    Determine the sum total of all numbers within the range ``l`` to
    ``r`` *inclusive* that can be written as a chunk of ``length`` digits
    repeated as many times as necessary.

    Preconditions:

    - ``l`` and ``r`` have the same length.
    - ``l`` and ``r`` can be evenly divided into chunks of ``length`` digits.

    Arguments:

        l: the left hand end of the range (a ``str`` made entirely of digits).
        r: the right hand end of the range (a ``str`` made entirely of digits).
        length: the length of the repeated chunk.

    Returns:
        the sum of all such repeated chunk numbers within the given range.
    """
    lchunks = [int(l[i : i + length]) for i in range(0, len(l), length)]
    rchunks = [int(r[i : i + length]) for i in range(0, len(r), length)]

    # determine the first number that could potentially be repeated
    # n times and still fall within the target range.  This will
    # usually be the first chunk of the left hand end, except where
    # the next chunk-that-does-not-equal-the-first is greater.  For
    # example, if we're looking at 2 digit chunks and l is 1212130456
    # then 1212121212 would not fall within the range as 121212....
    # must be less than 121213...  In this case the first candidate
    # for a repeat would be 1313131313.  But if l were 1212110456
    # then 1212121212 is a valid candidate.
    ll = lchunks.pop(0)
    lr = next((chunk for chunk in lchunks if chunk != ll), ll)
    if ll < lr:
        ll += 1

    # Mirror image logic for the *last* candidate repeated chunk -
    # if the right endpoint is 1414116835 then the last candidate
    # repeat would be 1313131313, but if r = 1414156835 then
    # 1414141414 would fit.
    rl = rchunks.pop(0)
    rr = next((chunk for chunk in rchunks if chunk != rl), rl)
    if rl > rr:
        rl -= 1

    if rl < ll:
        # no valid repetitions in this range
        return 0

    # now we know the valid repeated *chunks*, the actual repeated
    # *numbers* are found by multiplying the chunks by this factor;
    # for chunks of length 2 this is 101010101 (for however many
    # chunks), for length 3 it's 1001001001, etc.
    repeat_factor = sum(10 ** (length * i) for i in range(len(l) // length))

    if False:
        # Debugging code - print out the actual repeating numbers
        # to compare with the brute-force method
        for i in range(ll, rl + 1):
            print(f"start: {start}, end: {end}, i: {i*repeat_factor}")

    # so the *sum* of the repeated numbers is
    # sum(x from ll to rl) * repeat_factor
    #
    # and since
    #
    # sum(x from ll to rl) = sum(x from 1 to rl) - sum(x from 1 to ll-1)
    #
    # and the formula for the sum of the first n natural numbers is
    # n(n+1)/2, this works out as
    #
    # = ((rl * (rl+1)) // 2) - ((ll-1) * ll) // 2)
    return (((rl * (rl + 1)) - ((ll - 1) * ll)) // 2) * repeat_factor


def main():
    with open("input", "r") as f:
        data = [tuple(pair.split("-", maxsplit=1)) for pair in f.readline().strip().split(",")]

    # Part 1: just the cases where the number splits into exactly two halves
    start_time = perf_counter()
    total_repeated = 0
    for start, end in data:
        for l, r in equal_magnitude_ranges(start, end):
            length, remainder = divmod(len(l), 2)
            if remainder == 0:
                total_repeated += sum_repeats(l, r, length)

    print(f"Part 1: {total_repeated=}")
    print(f"Time: {perf_counter() - start_time}")

    # Part 2: all possible_splits combined using the IEP
    start_time = perf_counter()
    total_repeated = 0
    for start, end in data:
        for l, r in equal_magnitude_ranges(start, end):
            for length, plusminus in possible_splits(len(l)):
                total_repeated += sum_repeats(l, r, length) * plusminus

    print(f"Part 2: {total_repeated=}")
    print(f"Time: {perf_counter() - start_time}")


if __name__ == "__main__":
    main()
