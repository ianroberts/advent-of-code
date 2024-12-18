import re


def all_muls():
    with open("input", "r") as f:
        program = f.read()

    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    total = sum(int(m[1]) * int(m[2]) for m in pattern.finditer(program))
    print(f"All mul instructions: {total}")


def enabled_only():
    with open("input", "r") as f:
        program = f.read()

    pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|(do)(n't)?\(\)")
    total = 0
    enabled = True
    for m in pattern.finditer(program):
        # we can find the three cases by structural pattern matching on the
        # groups tuple
        match m.groups():
            case (None, None, "do", None):
                enabled = True
            case (None, None, "do", "n't"):
                enabled = False
            case (x, y, None, None):
                # only the first and second groups matched -> mul()
                if enabled:
                    total += int(x) * int(y)

    print(f"Enabled muls only: {total}")


if __name__ == "__main__":
    all_muls()
    enabled_only()
