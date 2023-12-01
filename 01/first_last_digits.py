import re
import sys

def digits_only():
    calibration_sum = 0
    with open(sys.argv[1], "r") as f:
        for line in f:
            first_digit = re.search(r"\d", line).group()
            last_digit = re.search(r"\d", line[::-1]).group()
            calibration_sum += 10*int(first_digit) + int(last_digit)

    print(f"Sum (digits only) = {calibration_sum}")


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
forward_re = re.compile(r"(" + "|".join(forward_digits.keys()) + r")|\d")

reverse_digits = {word[::-1]: value for word, value in forward_digits.items()}
reverse_re = re.compile(r"(" + "|".join(reverse_digits.keys()) + r")|\d")


def digits_and_words():
    calibration_sum = 0
    with open(sys.argv[1], "r") as f:
        for line in f:
            match = forward_re.search(line)
            if match.group(1):
                first_digit = forward_digits[match.group(1)]
            else:
                first_digit = int(match.group())

            match = reverse_re.search(line[::-1])
            if match.group(1):
                last_digit = reverse_digits[match.group(1)]
            else:
                last_digit = int(match.group())

            calibration_sum += 10*first_digit + last_digit

    print(f"Sum (digits and words) = {calibration_sum}")


if __name__ == "__main__":
    digits_only()
    digits_and_words()
