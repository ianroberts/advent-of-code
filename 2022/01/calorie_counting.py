

def calories_per_elf():
    current_elf = []
    with open("input", "r") as f:
        for line in f:
            line = line.strip()
            if line:
                current_elf.append(int(line))
            elif current_elf:
                yield current_elf
                current_elf = []

    if current_elf:
        yield current_elf


def most_calories():
    return max(sum(e) for e in calories_per_elf())


def total_top_three():
    top_three = [0, 0, 0]
    for e in calories_per_elf():
        top_three.append(sum(e))
        top_three.sort(reverse=True)
        top_three.pop()

    return sum(top_three)



if __name__ == "__main__":
    print(f"Max calories carried by one elf: {most_calories()}")
    print(f"Total calories carried by the top three: {total_top_three()}")
