# Alternative implementation using find and rfind rather than regular expressions

# Part 1 - digits only
digits = [(str(i), i) for i in range(10)]

# Part 2 - digits and digits-as-words
digits_and_words = digits + [
    ('one', 1),
    ('two', 2),
    ('three', 3),
    ('four', 4),
    ('five', 5),
    ('six', 6),
    ('seven', 7),
    ('eight', 8),
    ('nine', 9),
]


def calibration(lookup_table):
    calibration_sum = 0
    with open("input", "r") as f:
        for line in f:
            # We are searching each line for the furthest left and furthest right positions
            # at which any "digit" (FSVO digit - depending on the lookup table) occurs, and
            # using the corresponding value from the table as the integer value of that digit
            first_digit = -1
            last_digit = -1

            # Start first_digit_pos to the right of any possible actual positions
            first_digit_pos = len(line)
            # Start last_digit_pos to the left of any possible actual positions
            last_digit_pos = -1

            for digit, value in lookup_table:
                # Find the first and last indexes (if any) of this digit in the line
                this_digit_first = line.find(digit)
                this_digit_last = line.rfind(digit)

                if this_digit_first >= 0 and this_digit_first < first_digit_pos:
                    # This digit is in the line and is further left than any we've seen so far
                    first_digit_pos = this_digit_first
                    first_digit = value
                if this_digit_last >= 0 and this_digit_last > last_digit_pos:
                    # This digit is in the line and is further right than any we've seen so far
                    last_digit_pos = this_digit_last
                    last_digit = value

            if first_digit >= 0 and last_digit >= 0:
                calibration_sum += 10*first_digit + last_digit
            else:
                print(f"No digits found in '{line}'")

    return calibration_sum


if __name__ == "__main__":
    # Part 1: digits only
    print(f"Calibration sum (digits only) = {calibration(digits)}")
    print(f"Calibration sum (digits and words) = {calibration(digits_and_words)}")
