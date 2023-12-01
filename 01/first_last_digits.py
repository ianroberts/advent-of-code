import re
import sys


# Part 1: find the first and last *digits* in each line, combine them as a
# two digit number and sum across all lines

def digits_only():
    calibration_sum = 0
    with open(sys.argv[1], "r") as f:
        for line in f:
            first_digit = re.search(r"\d", line).group()
            last_digit = re.search(r"\d", line[::-1]).group()
            calibration_sum += 10*int(first_digit) + int(last_digit)

    print(f"Sum (digits only) = {calibration_sum}")


# Part 2: as well as digits, look for digit-as-word.  So now the first "digit"
# is either a true digit or a word "one" to "nine", and the last digit is the
# first instance in the reversed string of either a true digit or the reverse
# spelling of "eno" to "enin"

forward_digits = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}
# Add mappings for the actual digits 0-9
forward_digits.update((str(i), i) for i in range(10))

forward_re = re.compile("|".join(forward_digits.keys()))

# Create a parallel mapping of the reverse of each digit string
# for lookup in the reversed input string
reverse_digits = {word[::-1]: value for word, value in forward_digits.items()}
reverse_re = re.compile("|".join(reverse_digits.keys()))


def digits_and_words():
    calibration_sum = 0
    with open(sys.argv[1], "r") as f:
        for line in f:
            first_digit = forward_digits[forward_re.search(line).group()]
            last_digit = reverse_digits[reverse_re.search(line[::-1]).group()]

            calibration_sum += 10*first_digit + last_digit

    print(f"Sum (digits and words) = {calibration_sum}")


if __name__ == "__main__":
    digits_only()
    digits_and_words()
