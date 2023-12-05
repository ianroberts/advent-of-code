import re


def parse_input():
    f = open("input", "r")
    lines = iter(f)
    stacklines = []
    for line in lines:
        line = line.rstrip()
        if len(line) == 0:
            break
        stacklines.insert(0, line)

    # at this point the "lines" iterator is pointing at the first move
    # instruction, and stacklines contains the lines representing stacks,
    # starting from the bottom
    stackoffsets = [m.start() for m in re.finditer(r"\d", stacklines.pop(0))]
    stacks = [[line[off] for line in stacklines if off < len(line) and line[off] != " "] for off in stackoffsets]

    def instructions():
        instr_re = re.compile(r"move (\d+) from (\d+) to (\d+)")
        for line in lines:
            match = instr_re.search(line)
            yield (int(match.group(1)), int(match.group(2))-1, int(match.group(3))-1)

        f.close()

    return stacks, instructions()


def top_crate_one_by_one():
    stacks, instrs = parse_input()
    for num, from_stack, to_stack in instrs:
        for _ in range(num):
            stacks[to_stack].append(stacks[from_stack].pop())

    return "".join(stack[-1] for stack in stacks)


def top_crate_bulk():
    stacks, instrs = parse_input()
    for num, from_stack, to_stack in instrs:
        stacks[to_stack].extend(stacks[from_stack][-num:])
        stacks[from_stack][-num:] = []

    return "".join(stack[-1] for stack in stacks)



if __name__ == "__main__":
    print(f"Moving one by one: {top_crate_one_by_one()}")
    print(f"Moving in bulk: {top_crate_bulk()}")