from string import ascii_letters


def duplicate_items():
    total_priorities = 0
    with open("input", "r") as f:
        for line in f:
            line = line.strip()
            left_items = set(line[0: len(line)//2])
            right_items = set(line[len(line)//2:])
            both_items = left_items.intersection(right_items)
            if len(both_items) == 1:
                total_priorities += ascii_letters.find(both_items.pop()) + 1
            else:
                print(f"{line}: {len(both_items)} items duplicated")

    return total_priorities


def common_badge():
    total_priorities = 0
    with open("input", "r") as f:
        itr = iter(l.strip() for l in f)
        for elf1, elf2, elf3 in zip(itr, itr, itr):
            badge_set = set(elf1).intersection(set(elf2)).intersection(set(elf3))
            if len(badge_set) == 1:
                total_priorities += ascii_letters.find(badge_set.pop()) + 1
            else:
                print(f"{elf1} {elf2} {elf3}: could not find unique badge")

    return total_priorities


if __name__ == "__main__":
    print(duplicate_items())
    print(common_badge())
