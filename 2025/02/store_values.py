# Brute-force method for part 2 that just loops through every number
# in every range looking for ones that are repeating patterns - the
# actual check for duplicates is a very cool trick I spotted on reddit
# where you concatenate the string with itself, then look for the first
# place with index 1 or greater where the _original_ string can be found.
# If that's anywhere other than the halfway point it means that the
# string is a repeating pattern, e.g.
#
# i = "123123123"
# i+i = "123123123123123123"
#           ^-------^
#   Original string starts at index 3, so it is a repeat of a 3-digit base
#
# I knocked this up quickly as a way to debug my more mathematical approach,
# but for the given input this approach is plenty fast enough.  For what
# it's worth, the debugging was successful; the bug was that the mathematical
# version was counting single digit IDs like "3", "4", etc., but an ID needs
# to be at least 2 digits (11, 22, ...) to be considered a repeating pattern.

from time import perf_counter


def main():
    with open("input", "r") as f:
        data = [tuple(pair.split("-", maxsplit=1)) for pair in f.readline().strip().split(",")]

    # Part 1 for completeness - just the splits into two halves
    start_time = perf_counter()
    dups = set()
    for start, end in data:
        for i in range(int(start), int(end) + 1):
            si = str(i)
            halflength, remainder = divmod(len(si), 2)
            if remainder == 0 and si[0:halflength] == si[halflength:]:
                if False:
                    # Debugging
                    print(f"start: {start}, end: {end}, i: {i}")
                dups.add(i)

    print(f"Part 1: total_repeated={sum(dups)}")
    print(f"Time: {perf_counter() - start_time}")

    # Part 2 - all possible repeats
    start_time = perf_counter()
    dups = set()
    for start, end in data:
        for i in range(int(start), int(end) + 1):
            si = str(i)
            if (si + si).index(si, 1) != len(si):
                if False:
                    # Debugging
                    print(f"start: {start}, end: {end}, i: {i}")
                dups.add(i)

    print(f"Part 2: total_repeated={sum(dups)}")
    print(f"Time: {perf_counter() - start_time}")


if __name__ == "__main__":
    main()
