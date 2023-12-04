import re


def winning_numbers_per_card():
    with open("input", "r") as f:
        for line in f:
            line = line.strip()
            _, numbers = line.split(":")
            winning, mine = numbers.split("|")
            winning_numbers = set(int(m.group()) for m in re.finditer(r"\d+", winning))
            my_numbers = set(int(m.group()) for m in re.finditer(r"\d+", mine))
            yield winning_numbers.intersection(my_numbers)


def total_value():
    total_score = 0
    for my_winnings in winning_numbers_per_card():
        if my_winnings:
            total_score += 2 ** (len(my_winnings) - 1)

    return total_score


def copied_cards():
    total_count = 0
    # if we are currently looking at card N then copies[n] is the number of copies
    # of card N+n we have already accumulated
    copies = [0]

    for my_winnings in winning_numbers_per_card():
        # Remove this card from the copies stack and add 1 to get the total copies of this card
        this_card_count = 1 + (copies.pop(0) if len(copies) else 0)
        # add the total copies of this card to the running total
        total_count += this_card_count
        # X winning numbers on this card nets us this_card_count copies of the next X cards
        for n in range(len(my_winnings)):
            if n < len(copies):
                copies[n] += this_card_count
            else:
                copies.append(this_card_count)

    return total_count


if __name__ == "__main__":
    print(f"Total value: {total_value()}")
    print(f"Total cards including copies: {copied_cards()}")
