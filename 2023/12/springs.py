from functools import cache


debugging = False

def dbg(*args):
    if debugging:
        print(*args)


def input_lines(replicate=1):
    with open("input", "r") as f:
        for line in f:
            line = line.strip()
            pattern, runs_str = line.split()
            pattern = "?".join(pattern for _ in range(replicate))
            runs_str = ",".join(runs_str for _ in range(replicate))
            # Add a working spring to the end of the line to avoid edge cases
            pattern += "."
            runs = tuple(int(x) for x in runs_str.split(","))

            yield pattern, runs


calls = 0

# For part 1 I originally did the naive recursion without @cache.  That wasn't feasible for part 2
# but there's a *lot* of repeated work in the backtracking so adding @cache sped it up to just
# a couple of seconds by effectively turning the recursive algorithm into a dynamic programming one.
# Without @cache the "small world" version required 222754 total calls to count_possibilities,
# *with* @cache that fell to 51614.  Two or more repetitions didn't complete at all without @cache.
@cache
def count_possibilities(pattern, required_runs, cur_run=0):
    global calls
    calls += 1
    # go as far as we can through the string until we reach a decision point (?)
    while pattern:
        if pattern[0] == ".":
            if cur_run > 0:
                # we were in a run prior to this dot
                if not required_runs or required_runs[0] != cur_run:
                    # we've reached the end of a run, but we were expecting more damaged springs - fail
                    return 0

                # we've reached the end of a valid run
                required_runs = required_runs[1:]
                cur_run = 0
        elif pattern[0] == "#":
            # we are in a run now
            cur_run += 1
            if not required_runs or (cur_run > required_runs[0]):
                # we're gone too far for the current run to be valid - fail
                return 0
        elif pattern[0] == "?":
            # decision point - add up the possibilities for either option
            return (
                count_possibilities("#" + pattern[1:], required_runs, cur_run) +
                count_possibilities("." + pattern[1:], required_runs, cur_run)
            )

        pattern = pattern[1:]

    # we've run out of pattern characters
    if required_runs:
        # but we're still looking for another run - fail
        dbg(f"Fail - still need runs of {required_runs}")
        return 0
    else:
        # out of characters _and_ finished all runs - success
        dbg("Success")
        return 1


def all_possibilities(replicate=1):
    return sum(count_possibilities(pattern, runs) for pattern, runs in input_lines(replicate))


if __name__ == "__main__":
    for i in range(1, 6):
        calls = 0
        print(f"Total possibilities ({i}): {all_possibilities(i)} (took {calls} calls)")
