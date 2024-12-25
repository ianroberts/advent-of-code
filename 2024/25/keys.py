from itertools import product


def load_data():
    with open("input", "r") as f:
        keys = []
        locks = []
        def process_item(item: list[str]):
            target_list = locks
            if item[0][0] == ".":
                item.reverse()
                target_list = keys
            target_list.append(tuple(col.index(".") for col in zip(*item)))


        cur_item = []
        for line in f:
            line = line.strip()
            if line:
                cur_item.append(line)
                continue
            process_item(cur_item)
            cur_item = []

        if cur_item:
            process_item(cur_item)

    return locks, keys


def check_fit():
    locks, keys = load_data()

    print(locks[0], keys[0])

    compatible_pairs = 0
    for lock, key in product(locks, keys):
        if all(a + b <= 7 for a, b in zip(lock, key)):
            compatible_pairs += 1

    print(f"Total compatible lock/key pairs: {compatible_pairs}")


if __name__ == "__main__":
    check_fit()
