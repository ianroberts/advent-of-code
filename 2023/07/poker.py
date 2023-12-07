from collections import namedtuple
Hand = namedtuple("Hand", ["signature", "cards", "bid"])


# relative value of each card
values = {str(i): i for i in range(2, 10)}
values.update({
    'T': 10, 'J': 11, 'Q':12, 'K': 13, 'A': 14,
})
# joker - weaker than 2
values["j"] = 1


def to_hand(line, j_is_joker):
    cards_str, bid = line.split()
    if j_is_joker:
        cards_str = cards_str.replace("J", "j")

    # first map card names to integer values for ease of comparison
    cards = [values[card] for card in cards_str]
    # calculate a "signature" of the hand, made up of the count of each distinct
    # card type in the hand, ordered from highest to lowest count.  So the signature
    # for five of a kind will be [5], 4 of a kind [4, 1], FH [3, 2], 3oak [3, 1, 1],
    # two-pair [2, 2, 1], pair [2, 1, 1, 1] and high-card [1, 1, 1, 1, 1].  These
    # conveniently sort lexicographically matching the relative strengths.
    #
    # Jokers are special, they can impersonate any other card.  So we just count them
    # to start with, then process them at the end
    signature = []
    last_card = ""
    jokers = 0
    for card in sorted(cards):
        if card == 1:
            jokers += 1
        elif card == last_card:
            signature[-1] += 1
        else:
            signature.append(1)
            last_card = card
    signature.sort(reverse=True)  # reverse => highest to lowest

    # Deal with jokers - each joker impersonates whatever non-joker card has the highest
    # count.  If _all_ cards are jokers then they can all impersonate Aces and we have
    # five of a kind
    if signature:
        signature[0] += jokers
    else:
        signature.append(5)

    # Final representation of a hand is a tuple of signature, cards, bid.
    # The natural sort order of these tuples matches the strength rules described
    # in the puzzle, sorting by signature first, then breaking ties by relative
    # value of the cards one by one
    return Hand(signature, cards, int(bid))


def parse_input(jokers):
    with open("input", "r") as f:
        return [to_hand(line.strip(), jokers) for line in f]


def total_winnings(jokers):
    hands = parse_input(jokers)
    hands.sort()
    # hands is now ordered from weakest to strongest
    total = 0
    for i, hand in enumerate(hands):
        print(hand)
        total += (i+1) * hand.bid

    return total


if __name__ == "__main__":
    print(f"Total winnings (no jokers): {total_winnings(False)}")
    print(f"Total winnings (with jokers): {total_winnings(True)}")
