import operator
from collections import defaultdict
from itertools import islice


def load_data():
    with open("input", "r") as f:
        return [int(line) for line in f]


def prng(n: int) -> int:
    n1 = n << 6
    n = (n ^ n1) & 0xFFFFFF
    n2 = n >> 5
    n = (n ^ n2) & 0xFFFFFF
    n3 = n << 11
    n = (n ^ n3) & 0xFFFFFF

    return n


def part1():
    seeds = load_data()

    total = 0
    for seed in seeds:
        for n in range(2000):
            seed = prng(seed)
        total += seed

    print(f"Total of 2000th numbers: {total}")


def part2():
    seeds = load_data()

    all_prices = defaultdict(int)

    for seed in seeds:
        diffs = []
        prices = []
        for n in range(2000):
            new_seed = prng(seed)
            prices.append(new_seed % 10)
            diffs.append(new_seed % 10 - seed % 10)
            seed = new_seed

        # this_buyer_sequences is a sliding window over this buyer's PRNG sequence,
        # returning tuples of four items - (0, 1, 2, 3), (1, 2, 3, 4), (2, 3, 4, 5) ...
        this_buyer_sequences = zip(
            diffs,
            islice(diffs, 1, None),
            islice(diffs, 2, None),
            islice(diffs, 3, None),
        )
        # Current price at the _first_ appearance of each 4-tuple
        this_buyer_prices = {}
        for price, seq in zip(islice(prices, 3, None), this_buyer_sequences):
            if seq not in this_buyer_prices:
                this_buyer_prices[seq] = price

        # Update the global totals map from this buyer's numbers
        for seq, price in this_buyer_prices.items():
            all_prices[seq] += price

    max_bananas = max(all_prices.items(), key=operator.itemgetter(1))
    print(f"Max obtainable bananas: {max_bananas}")


if __name__ == "__main__":
    part1()
    part2()
