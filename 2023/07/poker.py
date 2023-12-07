from collections import namedtuple, Counter
Hand = namedtuple("Hand", ["signature", "cards", "bid"])


# relative value of each card
values = {str(i): i for i in range(2, 10)}
values.update({
    'T': 10, 'J': 11, 'Q':12, 'K': 13, 'A': 14,
})
# joker - weaker than 2
values["j"] = 1


def to_hand(line, j_is_joker):
    cards, bid = line.split()
    if j_is_joker:
        cards = cards.replace("J", "j")

    # calculate a "signature" of the hand, made up of the count of each distinct
    # card type in the hand, ordered from highest to lowest count.  So the signature
    # for five of a kind will be [5], 4 of a kind [4, 1], FH [3, 2], 3oak [3, 1, 1],
    # two-pair [2, 2, 1], pair [2, 1, 1, 1] and high-card [1, 1, 1, 1, 1].  The natural
    # lexicographic sort order of these lists matches the order of the hand types in the
    # puzzle.
    #
    count = Counter(cards)

    # Jokers are special, they can impersonate any other card.  So we just remove them
    # from the general counter first...
    jokers = count.pop("j", 0)
    # ... compute the basic signature without any jokers ...
    signature = sorted(count.values(), reverse=True)

    # Now the jokers - each joker impersonates whatever non-joker card has the highest
    # count.  If the signature is empty that means _all_ cards are jokers, so we have
    # five of a kind
    if signature:
        signature[0] += jokers
    else:
        signature.append(5)

    # Final representation of a hand is a tuple of signature, cards (mapped to
    # numeric values representing their relative rank), and bid value.
    # As with lists, tuples sort lexicographically, first comparing the
    # leftmost item, then if those are equal the next, etc.  Therefore the natural
    # sort order of these "hand" tuples matches the strength rules described
    # in the puzzle, sorting first by signature, then breaking ties by the relative
    # value of the cards from left to right
    return Hand(signature, [values[card] for card in cards], int(bid))


def parse_input(jokers):
    with open("input", "r") as f:
        return [to_hand(line.strip(), jokers) for line in f]


def total_winnings(jokers):
    hands = parse_input(jokers)
    hands.sort()
    # hands is now ordered from weakest to strongest
    total = 0
    for i, hand in enumerate(hands):
        print(f"  Rank {i+1:4d}: {hand}")
        total += (i+1) * hand.bid

    return total


if __name__ == "__main__":
    print(f"Total winnings (no jokers): {total_winnings(False)}")
    print(f"Total winnings (with jokers): {total_winnings(True)}")
