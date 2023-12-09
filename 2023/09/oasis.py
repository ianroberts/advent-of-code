

def parse_input():
    with open("input", "r") as f:
        for line in f:
            yield [int(val) for val in line.split()]


def extrapolate():
    sum_of_new_values = 0
    for seq in parse_input():
        row = seq
        diffs = []
        all_zero = False
        while not all_zero:
            diffs.append(row)
            row = [row[i+1] - row[i] for i in range(len(row) - 1)]
            all_zero = all(val == 0 for val in row)

        # Starting from zero...
        new_val = 0
        for d in reversed(diffs):
            # Add the result from last time around (the (n-1)th order difference)
            # to the last value in the current sequence
            new_val = new_val + d[-1]

        # When we run out of rows we're left with the value we wanted to start with
        sum_of_new_values += new_val

    return sum_of_new_values


def extrapolate_back():
    sum_of_new_values = 0
    for seq in parse_input():
        # computing the diffs is the same as part 1
        row = seq
        diffs = []
        all_zero = False
        while not all_zero:
            diffs.append(row)
            row = [row[i+1] - row[i] for i in range(len(row) - 1)]
            all_zero = all(val == 0 for val in row)

        # Starting from zero...
        new_val = 0
        for d in reversed(diffs):
            # *Subtract* the result from last time around (the (n-1)th order difference)
            # from the *first* value in the current sequence
            new_val = d[0] - new_val

        # When we run out of rows we're left with the value we wanted to start with
        sum_of_new_values += new_val

    return sum_of_new_values


if __name__ == "__main__":
    print(f"Sum of extrapolated end values: {extrapolate()}")
    print(f"Sum of extrapolated start values: {extrapolate_back()}")

