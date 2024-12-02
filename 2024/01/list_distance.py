from collections import Counter


def load_lists():
    # There's probably a more pythonic way to do this with zip etc. but
    # given that I need everything as lists I can sort rather than immutable
    # tuples I'll go with this
    with open("input", "r") as f:
        list1 = []
        list2 = []
        for line in f:
            v1, v2 = (int(v) for v in line.split())
            list1.append(v1)
            list2.append(v2)
    return list1, list2


def min_distance():
    list1, list2 = load_lists()
    list1.sort()
    list2.sort()

    print(f"Min distance: {sum(abs(v1-v2) for v1, v2 in zip(list1, list2))}")


def similarity():
    list1, list2 = load_lists()
    # Counter gives you a mapping from value to number-of-occurrences
    count1 = Counter(list1)
    count2 = Counter(list2)

    # The similarity score for each _distinct_ entry N in list 1 is N times the
    # count of Ns in list 2, then we need to multiply by the number of times that
    # number was seen in list 1.
    print(f"Similarity: {sum(n1 * cnt1 * count2[n1] for n1, cnt1 in count1.items())}")


if __name__ == "__main__":
    min_distance()
    similarity()
